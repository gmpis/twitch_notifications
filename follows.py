import requests
import os
import pprint
import json

# pr_pr = pprint.PrettyPrinter(indent=4)

# config var TODO edit with the selected name/id
# l_user_str = "twitch"     # extra, sting usernames that the user_id belongs to
l_user_id = "0"             # id from the user we want to read follows

# tmp_vars
total_follows = 1  # total number of users the current user is following
read_follows = 0   # number of follows read untill now, init to 0

# read env vars
# base_url = "https://api.twitch.tv/kraken/users"
full_url = "https://api.twitch.tv/kraken/users/" + l_user_id + "/follows/channels"
# to set environment variables use: export M_API_KEY=000000
g_client_id = os.getenv("OAUTH_CLIENT_ID", "000000")  # read client_id from env vars, defaults to 000000, invalid
m_headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": g_client_id}  # Accept header is required, selects v5 API
m_params = {"limit": 100, "offset": 0, "direction": "desc", "sortby": "created_at"}  # query params: ?key=value

m_resp = requests.get(full_url, headers=m_headers, params=m_params)   # , timeout=m_timeout)
if m_resp.status_code == requests.codes.ok:
    # print(m_resp.headers)
    # print(m_resp.text)

    m_resp_json = m_resp.json()  # class 'dict'
    # pr_pr.pprint(m_resp_json)  # pretty print response data

    users_lst = m_resp_json  #["users"]
    str_body = json.dumps(users_lst)  # get only users list, too inefficient
    print(str_body)

    # for tmp_u in users_lst:
    #     do something with the data here ...
    #     print(tmp_u)


else:
    print("Sorry something went wrong...")
    print("Status code: " + str(m_resp.status_code) + "\n" + str(m_resp.text))

# print("Done, exiting now ...")
