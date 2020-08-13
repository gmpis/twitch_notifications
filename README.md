# twitch_notifications  

##  How to use: server side  
- deploy webhook server `t_webhook.py`  
- set the env var: `export DISCORD_URL=123`  

## How to use: client side  
- set the env vars:  
`export OAUTH_CLIENT_ID=123`  
`export OAUTH_TOKEN=123`  
`export CALLBACK_URL=http://localhost/webhook/`  
- add the names of the channels you want to, on l_csv_users_str variable at search.py file  
- run search script as: `python3 search.py | tee users.json`  
- run register script as: `python3 register.py`  