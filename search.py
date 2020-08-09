import requests
import os
import pprint
import json

pr_pr = pprint.PrettyPrinter(indent=4)

# config var TODO edit with the selected names
l_csv_users_str = "user1,user2"  # sting (list) of usernames to search their IDs, separated by ","

base_url = "https://api.twitch.tv/kraken/users"
g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id from env vars, defaults to 000000, invalid
# to set environment variables use: export M_API_KEY=000000
m_headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": g_client_id}  # Accept header is required, selects v5 API
m_params = {"login": l_csv_users_str}  # ?key=value
# m_timeout = 1  # in sec


m_resp = requests.get(base_url, headers=m_headers, params=m_params)   # , timeout=m_timeout)
if m_resp.status_code == requests.codes.ok:
    # print(m_resp.headers)
    # print(m_resp.text)

    m_resp_json = m_resp.json()  # class 'dict'
    # pr_pr.pprint(m_resp_json)  # pretty print response data

    users_lst = m_resp_json["users"]
    str_body = json.dumps(users_lst)  # get only users list, too inefficient
    print(str_body)

    # for tmp_u in users_lst:
    #     do something with the data here ...
    #     print(tmp_u)


else:
    print("Sorry something went wrong...")
    print("Status code: " + str(m_resp.status_code) + "\n" + str(m_resp.text))

print("Done, exiting now ...")
