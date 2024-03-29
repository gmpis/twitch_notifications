import requests
import os
import json
# import pprint

# read values from env vars
g_app_token = os.getenv("APP_TOKEN", "abc")  # generated using client credentials flow
g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id, defaults to 000000, invalid
g_oauth_token = os.getenv("OAUTH_TOKEN", "abc")  # oauth_token for the signed in user,
g_callback_url = os.getenv("CALLBACK_URL", "")      # read callback_url, webhook url of our server that accepts notifications, must end in .com, .gr etc
g_secret = os.getenv("HUB_SECRET", "abc")           # used from twitch to sign notifications, TODO must be 10+ characters

# my vars
registr_version = "EVENTSUB"  # choose registration type opt: "EVENTSUB", "WEBHOOK",
eventsub_log = []  # list that contain a log of eventsub responses
# pr_pr = pprint.PrettyPrinter(indent=4)


def register_stream_webhook(l_channel_id, l_channel_name):
    # g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id, defaults to 000000, invalid
    # g_oauth_token = os.getenv("OAUTH_TOKEN", "abc")  # oauth_token for the signed in user,
    # g_callback_url = os.getenv("CALLBACK_URL", "")  # read callback_url, webhook url of our server that accepts notifications, must end /
    # g_callback_url ==  "www. ... .com"
    full_callback_url = g_callback_url + "/webhook/" + l_channel_name + "/"  # overwrite with full url, eg: "http://localhost/webhook/" + "nasa" + "/"
    # g_secret = os.getenv("HUB_SECRET", "abc")  # used from twitch to sign notifications

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


def register_eventsub_webhook(l_channel_id, l_channel_name, l_eventsub_log):
    # g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id, defaults to 000000, invalid
    # g_oauth_token = os.getenv("OAUTH_TOKEN", "abc")  # oauth_token for the signed in user,
    # g_callback_url = os.getenv("CALLBACK_URL", "")  # read callback_url, webhook url of our server that accepts notifications, must end /
    # g_secret = os.getenv("HUB_SECRET", "abc")  # used from twitch to sign notifications
    print("Processing: " + l_channel_name +":")
    # g_callback_url ==  "www. ... .com"
    full_callback_url = g_callback_url + "/eventsub/" + l_channel_name + "/"  # overwrite with full url, eg: "http://localhost/eventsub/" + "nasa" + "/"

    # request config
    base_url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    tmp_auth_header = "Bearer " + g_app_token
    m_headers = {"Client-ID": g_client_id, "Authorization": tmp_auth_header}  # , "Content-Type": "text/plain"} , change to json

    # init once, same for all events
    m_transport_dict = {"method": "webhook", "callback": full_callback_url, "secret": g_secret}

    # Register online webhook here
    m_cond_d = {"broadcaster_user_id": l_channel_id}
    m_body = {"type": "stream.online", "version": "1", "condition": m_cond_d,  "transport": m_transport_dict}

    m_resp = requests.post(base_url, headers=m_headers, json=m_body)
    # if m_resp.status_code == requests.codes.ok:  # must be 202
    if m_resp.status_code == 202:  # must be 202, DONT use: requests.codes.ok
        print("\t-Registered: " + l_channel_name + " stream.online successfully !!!")
        # read body, not empty
        registr_body = m_resp.json()
        # print(registr_body)
        l_eventsub_log.append(registr_body)
    else:
        print("Twitch Error registering: " + l_channel_name + " stream.online, Status:" + str(m_resp.status_code))
        print(m_resp.text)

    # Register offline webhook here
    m_cond_d = {"broadcaster_user_id": l_channel_id}
    m_body = {"type": "stream.offline", "version": "1", "condition": m_cond_d,  "transport": m_transport_dict}

    m_resp = requests.post(base_url, headers=m_headers, json=m_body)
    # if m_resp.status_code == requests.codes.ok:  # must be 202
    if m_resp.status_code == 202:  # must be 202, DONT use: requests.codes.ok
        print("\t-Registered: " + l_channel_name + " stream.offline successfully !!!")
        # read body, not empty
        registr_body = m_resp.json()
        # print(registr_body)
        l_eventsub_log.append(registr_body)
    else:
        print("Twitch Error registering: " + l_channel_name + " stream.offline, Status:" + str(m_resp.status_code))
        print(m_resp.text)

    # Register raid webhook here
    m_cond_d = {"from_broadcaster_user_id": l_channel_id}
    m_body = {"type": "channel.raid", "version": "beta", "condition": m_cond_d,  "transport": m_transport_dict}

    m_resp = requests.post(base_url, headers=m_headers, json=m_body)
    # if m_resp.status_code == requests.codes.ok:  # must be 202
    if m_resp.status_code == 202:  # must be 202, DONT use: requests.codes.ok
        # print("Twitch POST was successful!")
        print("\t-Registered: " + l_channel_name + " channel.raid successfully !!!")
        # read body, not empty
        registr_body = m_resp.json()
        # print(registr_body)
        l_eventsub_log.append(registr_body)
    else:
        print("Twitch Error registering: " + l_channel_name + " channel.raid, Status:" + str(m_resp.status_code))
        print(m_resp.text)

    print("Done " + l_channel_name +" !!!")


if __name__ == "__main__":
    f_name = "./users.json"

    # TODO if cli param overwrite f_name

    # read file
    f = open(f_name)
    f_contents = f.read()
    json_users = json.loads(f_contents)

    for tmp_u in json_users:
        tmp_name = tmp_u["name"]
        tmp_id = tmp_u["_id"]
        # print(tmp_u)
        # print("user: " + tmp_name + ", with id: " + tmp_id)
        if registr_version == "EVENTSUB":
            # latest version
            register_eventsub_webhook(tmp_id, tmp_name, eventsub_log)
        elif registr_version == "WEBHOOK":
            # old version
           register_stream_webhook(tmp_id, tmp_name)
        else:
            # Unknown type, do nothing
            pass

    # if we have log, print it
    if len(eventsub_log) > 0:
        print(eventsub_log)

    # registered all users close file
    f.close()
