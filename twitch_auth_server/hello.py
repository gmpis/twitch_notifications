from flask import Flask, redirect, request  #, url_for
import os
import urllib.parse
import requests as ex_requests
import redis
import time
import json


m_db_conn = ""  # connection to db, init to empty
l_use_db = os.getenv("USE_DB", "")  # defaults to empty, dont store any resp on db
if l_use_db:
    # for more control change to: if l_use_db == "True":
    l_db_host = os.getenv("DB_HOST", "localhost")  # db host
    l_db_port = os.getenv("DB_PORT", "6379")    # db port
    # l_db_user = os.getenv("DB_USER", "")      # db username
    l_db_pass = os.getenv("DB_PASS", "")        # db password
    # end config

    print("Connecting to db ...")
    m_db_conn = redis.Redis(host=l_db_host, port=l_db_port, password=l_db_pass)

    # test db connection
    l_curr_millisec = int(time.time()) * 1000  # current time in milliseconds, (since Epoch)
    m_db_conn.set("last_conn", l_curr_millisec)  # log most recent connection


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/start')
def start_oauth():

    # read values from env vars
    l_state = 111111  # TODO generate random value, used to maintain state and prevent csrf attacks

    l_client_id = os.getenv("OAUTH_CLIENT_ID", "12345")  # from dev portal
    l_redirect_url = os.getenv("REDIRECT_URL", "http://localhost")  # url for callback (this server), case sensitive and must match value registered on dev portal
    # scope param is not supported, must be declared on dev portal

    # create url from vars
    l_dict = {"response_type": "code", "client_id": l_client_id, "state": l_state, "redirect_uri": l_redirect_url}
    l_params = urllib.parse.urlencode(l_dict)

    auth_base_url = "https://id.twitch.tv/oauth2/authorize?%s" % l_params

    # print(l_params)
    # print(auth_base_url)
    # return "DEV:"+auth_base_url

    # do redirect
    return redirect(auth_base_url)


@app.route('/callback', methods=["GET", "POST"])
def callback_oauth():
    """ Implements Authorization code flow """
    # log incoming request
    print(request.method)  # "GET", "POST"
    print(request.args)  # access url params ?key=123 eg: request.args.get("key", ""))
    print(request.form)  # access form data posted to this endpoint, eg: request.form["user"]

    # read values from url params
    l_code = request.args.get("code", "0")  # get code from request
    l_state = request.args.get("state", "111111")  # get state from request, is same value that was set on /start'
    # read values from env vars
    l_client_id = os.getenv("OAUTH_CLIENT_ID", "12345")  # from dev portal
    l_client_secret = os.getenv("OAUTH_CLIENT_SECRET", "12345")  # from dev portal
    l_redirect_url = os.getenv("REDIRECT_URL", "http://localhost")  # url for callback (this server), case sensitive and must match value registered on dev portal

    # create request from vars
    l_dict = {"grant_type": "authorization_code", "code": l_code, "client_id": l_client_id, "client_secret": l_client_secret, "redirect_uri": l_redirect_url}
    auth_token_url = "https://id.twitch.tv/oauth2/token"

    # do post request to get token
    m_access_token = ""
    m_resp = ex_requests.post(auth_token_url, data=l_dict)  # post data as x-www-form-urlencoded
    if m_resp.status_code == ex_requests.codes.ok:
        print("Post was successful!")
        full_json_body = m_resp.json()
        print(full_json_body)
        # print(type(full_json_body))  # class dict

        # extract token from response
        m_access_token = full_json_body["access_token"]

        # extract refresh token from response
        m_refresh_token = full_json_body["refresh_token"]

        # save refresh token to db
        if l_use_db:
            l_db_key = l_state  # TODO SOS check key_name (input) before saving to db, to avoid attacks

            tmp_curr_millisec = int(time.time()) * 1000  # current time in milliseconds, (since Epoch)
            tmp_u_json = full_json_body
            tmp_u_json["w_rec_time"] = str(tmp_curr_millisec)  # millisec the token was generated / received
            tmp_db_value = json.dumps(tmp_u_json)
            # print(tmp_db_value)  # class string

            m_db_conn.set(l_db_key, tmp_db_value)  # store user token to db
    else:
        print("Res:"+m_resp.text)
        return "Error couldn\'t get access token"

    # return token
    return "Access token: "+m_access_token


@app.route('/refresh/<string:db_key>/', methods=["GET", "POST"])
def refresh_oauth(db_key):

    if l_use_db:
        # TODO SOS check input before searching, vuln
        resp_bytes = m_db_conn.get(db_key)  # search db for db_key, returns: class 'bytes'

        if resp_bytes:  # TODO look again condition
            # key exists and received valid response from db
            resp_str = resp_bytes.decode("utf-8")  # class 'str', convert bytes to string
            resp_dec = json.loads(resp_str)  # class 'dict'

            # extract refresh token
            prev_refresh_token = resp_dec["refresh_token"]
            # print(prev_refresh_token)
            # return resp_str

            # read values from env vars
            l_client_id = os.getenv("OAUTH_CLIENT_ID", "12345")  # from dev portal
            l_client_secret = os.getenv("OAUTH_CLIENT_SECRET", "12345")  # from dev portal

            # create request from vars
            l_dict = {"grant_type": "refresh_token", "refresh_token": prev_refresh_token, "client_id": l_client_id, "client_secret": l_client_secret}
            l_headers = {"Content-Type": "application/x-www-form-urlencoded"}
            auth_token_url = "https://id.twitch.tv/oauth2/token"

            # do post request to refresh token
            m_resp = ex_requests.post(auth_token_url, headers=l_headers, data=l_dict)  # post data as x-www-form-urlencoded
            if m_resp.status_code == ex_requests.codes.ok:
                print("(Refresh) Post was successful!")
                full_json_body = m_resp.json()
                print("After: " + str(full_json_body))
                # print(type(full_json_body))  # class dict

                # extract token from response
                m_access_token = full_json_body["access_token"]

                # save refresh token to db, checked for db usage at the beginning
                tmp_curr_millisec = int(time.time()) * 1000  # current time in milliseconds, (since Epoch)
                tmp_u_json = full_json_body
                tmp_u_json["w_refred_time"] = str(tmp_curr_millisec)  # millisec the token was generated / received
                tmp_db_value = json.dumps(tmp_u_json)
                # print(tmp_db_value)  # class string

                m_db_conn.set(db_key, tmp_db_value)  # store user token to db
                return tmp_db_value
            else:
                print("Error, status: " + str(m_resp.status_code) + " with body: " + m_resp.text)
                return "Error Couldn\'t refresh token received status : %s" % m_resp.status_code

        else:
            # TODO SOS check input before returning, reflection vuln
            return "Couldn\'t find: %s" % db_key
    else:
        return "Under construction!"


@app.route('/revoke/<string:db_key>/', methods=["GET", "POST"])
def revoke_oauth(db_key):
    return "Under construction!"
