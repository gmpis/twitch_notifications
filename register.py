import requests
import os
# import pprint
# import json

# pr_pr = pprint.PrettyPrinter(indent=4)

# read values from env vars
g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id, defaults to 000000, invalid
g_oauth_token = os.getenv("OAUTH_TOKEN", "abc")
g_callback_url = os.getenv("CALLBACK_URL", "")  # read callback_url, webhook url of our server that accepts notifications
g_secret = os.getenv("HUB_SECRET", "abc")  # used from twitch to sign notifications

base_url = "https://api.twitch.tv/helix/webhooks/hub"

tmp_auth_header = "Bearer " + g_oauth_token
m_headers = {"Client-ID": g_client_id, "Authorization": tmp_auth_header, "Content-Type": "text/plain"}

tmp_user_id = 0  # TODO set real id
l_topic = "https://api.twitch.tv/helix/streams?user_id=%s" % tmp_user_id
m_body = {"hub.callback": g_callback_url, "hub.mode": "subscribe", "hub.topic": l_topic,  "hub.lease_seconds": 864000, "hub.secret": g_secret}

m_resp = requests.post(base_url, headers=m_headers, data=m_body)
if m_resp.status_code == requests.codes.ok:  # must be 202
    print("Twitch POST was successful!")
    # body must be empty
else:
    print("Twitch Error status:" + str(m_resp.status_code))
    print(m_resp.text)

print("Done, exiting now ...")
