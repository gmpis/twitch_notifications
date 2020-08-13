import requests
import os
# import pprint
# import json

# pr_pr = pprint.PrettyPrinter(indent=4)


# read values from env vars
def register_stream_webhook(l_channel_id, l_channel_name):
    g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id, defaults to 000000, invalid
    g_oauth_token = os.getenv("OAUTH_TOKEN", "abc")  # oauth_token for the signed in user,
    g_callback_url = os.getenv("CALLBACK_URL", "")  # read callback_url, webhook url of our server that accepts notifications, must end /
    full_callback_url = g_callback_url + l_channel_name + "/"  # overwrite with full url, eg: "http://localhost/webhook/" + "nasa" + "/"
    g_secret = os.getenv("HUB_SECRET", "abc")  # used from twitch to sign notifications

    base_url = "https://api.twitch.tv/helix/webhooks/hub"

    tmp_auth_header = "Bearer " + g_oauth_token
    m_headers = {"Client-ID": g_client_id, "Authorization": tmp_auth_header}  # , "Content-Type": "text/plain"} , change to json

    # tmp_user_id = 0  # set real id
    l_topic = "https://api.twitch.tv/helix/streams?user_id=%s" % l_channel_id
    m_body = {"hub.callback": full_callback_url, "hub.mode": "subscribe", "hub.topic": l_topic,  "hub.lease_seconds": 864000, "hub.secret": g_secret}

    m_resp = requests.post(base_url, headers=m_headers, json=m_body)
    # if m_resp.status_code == requests.codes.ok:  # must be 202
    if m_resp.status_code == 202:  # must be 202, DONT use: requests.codes.ok
        print("Twitch POST was successful!")
        print("Registered: " + l_channel_name + " successfully !!!")
        # body must be empty
    else:
        print("Twitch Error registering: " + l_channel_name + " Status:" + str(m_resp.status_code))
        print(m_resp.text)

    print("Done !!!")


register_stream_webhook("12826", "Twitch")
