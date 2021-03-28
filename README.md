# twitch_notifications  

## Setup Discord   
- Login to Discord and create a new Discord server   
- create a new text channel   
- right click on the channel > Edit Channel > Integrations > Webhooks > Create Webhook   
- set a name, and a profile picture for the Bot   
- click Copy Webhook URL, we need the url to set the webhook server    
   
## Setup Twitch    
- Login to Twitch and enable 2FA (required)   
- Register a new application on the dev portal   
   
## Install dev dependencies   
`pip3 install -r requirements.txt`   
   
Note: *If you haven't already installed pip/pip3, you can do so by running: `sudo apt install python3-pip`*   

##  How to use: server side  
- deploy webhook server `t_webhook.py`  
- set the env var: `export DISCORD_URL=123`  

## How to use: client side  
Note: *The following steps must be performed AFTER the web server has been deployed AND configured!!! *   
- set the env vars:  
`export OAUTH_CLIENT_ID=123`  
`export OAUTH_TOKEN=123`  
  or depending on registration version: `export APP_TOKEN=123`  
`export CALLBACK_URL=http://localhost/`   
`export HUB_SECRET=abc`  
- add the names of the channels you want to, on l_csv_users_str variable at search.py file  
- run search script as: `python3 search.py | tee users.json`  
- run register script as: `python3 register.py`  

## Debug webhooks   
   
## TODO   
   