import requests
import os
import json
# import pprint

# read values from env vars
g_app_token = os.getenv("APP_TOKEN", "abc")  # generated using client credentials flow
g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id, defaults to 000000, invalid

# my vars
registr_version = "EVENTSUB"  # choose registration type opt: "EVENTSUB", "WEBHOOK",
eventsub_log = []  # list that contain a log of eventsub responses
# pr_pr = pprint.PrettyPrinter(indent=4)


def list_eventsub_webhooks(l_eventsub_log):
    """ List all registered webhooks """
    # config request
    base_url = "https://api.twitch.tv/helix/eventsub/subscriptions"

    tmp_auth_header = "Bearer " + g_app_token
    m_headers = {"Client-ID": g_client_id, "Authorization": tmp_auth_header}

    m_params_dict = {"status": "enabled"}  # query string for the request
    # alt options for status: ["enabled", "webhook_callback_verification_pending", "webhook_callback_verification_failed"
    #                            , "notification_failures_exceeded, "authorization_revoked", "user_removed"]

    # List webhooks here
    m_resp = requests.get(base_url, headers=m_headers, params=m_params_dict)
    # if m_resp.status_code == requests.codes.ok:  # must be 202
    if m_resp.status_code == 200:  # must be 202, DONT use: requests.codes.ok
        # here we have a json body with registered webhooks TODO handle pagination
        # read body, not empty
        registr_body = m_resp.json()
        # print(registr_body)
        l_eventsub_log.append(registr_body)
    else:
        print("Twitch Error listing webhooks, Status:" + str(m_resp.status_code))
        print(m_resp.text)

    print("Done !!!")


def delete_eventsub_webhook(l_webhook_id, l_eventsub_log):
    """ Delete a preregistered webhook with a given id"""
    # request config
    base_url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    tmp_auth_header = "Bearer " + g_app_token
    m_headers = {"Client-ID": g_client_id, "Authorization": tmp_auth_header}  # , "Content-Type": "text/plain"} , change to json
    m_params_dict = {"id": l_webhook_id}  # query string for the request
    # m_body = {"id": l_webhook_id}

    # Delete webhook here
    m_resp = requests.delete(base_url, headers=m_headers, params=m_params_dict)  # json=m_body,
    # if m_resp.status_code == requests.codes.ok:  # must be 202
    if m_resp.status_code == 204:  # must be 202, DONT use: requests.codes.ok
        print("Deleted: " + l_webhook_id + " webhook successfully !!!")
        # read body, not empty
        # registr_body = m_resp.json()
        # print(registr_body)
        # l_eventsub_log.append(registr_body)
    else:
        print("Twitch Error deleting webhook: " + l_webhook_id + ", Status:" + str(m_resp.status_code))
        print(m_resp.text)

    print("Done " + l_webhook_id +" !!!")


if __name__ == "__main__":
    # TODO if cli param overwrite f_name

    # read file
    # f_name = "./webhooks.json"
    # f = open(f_name)
    # f_contents = f.read()
    # json_users = json.loads(f_contents)

    # for tmp_u in json_users:
    #     tmp_name = tmp_u["name"]
    #     tmp_id = tmp_u["_id"]

    # list all registered webhooks
    list_eventsub_webhooks(eventsub_log)

    # delete webhooks
    tmp_delete_ids = []  # TODO fill with webhook ids you want to delete

    for tmp_id in tmp_delete_ids:
        delete_eventsub_webhook(tmp_id, eventsub_log)

    # if we have log, print it
    if len(eventsub_log) > 0:
        print("\n\n")  # some whitespace from prev print
        webhook_lst = eventsub_log
        str_body = json.dumps(webhook_lst)
        print(str_body)  #  json encoded body, can be written to a file

    # registered all users close file
    # f.close()
