from flask import Flask, request
import os
import requests as ex_requests
import json

# read values from env vars
l_discord_url = os.getenv("DISCORD_URL", "")
l_hub_secret = os.getenv("HUB_SECRET", "")

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/webhook/<string:user_name>/', methods=["GET", "POST"])
def accept_webhook(user_name):
    # incoming webhook

    if request.method == "GET":
        # verify subscription

        tmp_challenge = request.args.get("hub.challenge", "0")
        # TODO handle subscription deny: "hub.reason"

        fl_response = tmp_challenge  # echo the provided challenge
        fl_status = 200
        fl_headers = {"Content-Type": "text/plain"}
        return (fl_response, fl_status, fl_headers)

    else:
        # POST, receiving event
        # print(request.content_length)
        # TODO verify payload signature using l_hub_secret and sha256
        print(request.method)  # "GET", "POST"
        print(request.args)  # access url params ?key=123 eg: request.args.get("key", ""))
        print(request.headers)  # access http headers
        print(request.form)  # access form data posted to this endpoint, eg: request.form["user"]

        webhook_data = request.get_data()  # returns bytestring of incoming data, alt use request.get_json()
        out_str = "{\"" + user_name + "\" : \"" + webhook_data.decode("utf-8") + "\"}"
        out_json = json.dumps({"content": out_str})  # TODO do some cleanup
        # print(out_json)

        # post message to discord
        l_headers = {"Content-Type": "application/json"}
        m_resp = ex_requests.post(l_discord_url, headers=l_headers, data=out_json)
        if (m_resp.status_code == ex_requests.codes.ok) or (m_resp.status_code == 204):
            print("Discord POST was successful!")
        else:
            print("Discord Error status:" + str(m_resp.status_code))
            print(m_resp.text)

        fl_response = "OK"
        return (fl_response, 200)  # always return 200x else twitch server will retry to deliver the notification


@app.route('/eventsub/<string:user_name>/', methods=["GET", "POST"])
def accept_eventsub_webhook(user_name):
    # incoming webhook

    if request.method == "GET":
        # keep for debug, should not receive any requests here
        fl_response = "OK"
        fl_status = 200
        fl_headers = {"Content-Type": "text/plain"}
        return (fl_response, fl_status, fl_headers)

    else:
        # POST, receiving a notification or an eventsub verification request
        # print(request.content_length)
        # TODO verify payload signature using l_hub_secret and sha256
        print(request.method)  # "GET", "POST"
        print(request.args)  # access url params ?key=123 eg: request.args.get("key", ""))
        print(request.headers)  # access http headers
        print(request.form)  # access form data posted to this endpoint, eg: request.form["user"]

        webhook_data = request.get_json()  # request.get_json()

        m_msg_type = request.headers.get("Twitch-Eventsub-Message-Type")
        if m_msg_type == "webhook_callback_verification":
            # this is a verification request, handle it accordingly
            tmp_challenge = webhook_data["challenge"]

            fl_response = tmp_challenge  # echo the provided challenge
            fl_status = 200
            fl_headers = {"Content-Type": "text/plain"}
            return (fl_response, fl_status, fl_headers)

        else:
            # this is a notification
            # m_msg_type == "notification"
            disc_msg = ""  # message to be send to discord, init to empty
            # out_str = "{\"" + user_name + "\" : \"" + webhook_data.decode("utf-8") + "\"}"

            m_notif_type = webhook_data["subscription"]["type"]
            if m_notif_type == "stream.online":
                stream_title = ""
                event_data = webhook_data["event"]  # TODO debug, full event data
                disc_msg = user_name + " Started stream : " + stream_title + " : " + event_data.decode("utf-8")
            elif m_notif_type == "stream.offline":
                disc_msg = user_name + " went offline."
            elif m_notif_type == "channel.raid":
                # raid_snd = webhook_data["event"]["from_broadcaster_user_name"]
                raid_recv = webhook_data["event"]["to_broadcaster_user_name"]
                disc_msg = user_name + " is raiding: " + raid_recv
            else:
                # unknown type, dont send request to discord
                pass

            if disc_msg:
                # print(disc_msg)
                out_json = json.dumps({"content": disc_msg})  # TODO do some cleanup

                # post message to discord
                l_headers = {"Content-Type": "application/json"}
                m_resp = ex_requests.post(l_discord_url, headers=l_headers, data=out_json)
                if (m_resp.status_code == ex_requests.codes.ok) or (m_resp.status_code == 204):
                    print("Discord POST was successful!")
                else:
                    print("Discord Error status:" + str(m_resp.status_code))
                    print(m_resp.text)

            fl_response = "OK"
            return (fl_response, 200)  # always return 200x else twitch server will retry to deliver the notification
