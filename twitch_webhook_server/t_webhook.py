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
