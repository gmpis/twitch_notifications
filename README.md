# twitch_notifications  

## Setup Discord   
- Login to Discord and create a new Discord server   
- create a new text channel   
- right click on the channel > Edit Channel > Integrations > Webhooks > Create Webhook   
- set a name, and a profile picture for the Bot   
- click Copy Webhook URL, (we need to set this url as env var on webhook server)    
   
## Setup Twitch    
- Login to Twitch and enable 2FA (required)   
- Register a new application on the dev portal   
   
## Install dev dependencies   
`pip3 install -r requirements.txt`   
   
Note: *If you haven't already installed pip/pip3, you can do so by running: `sudo apt install python3-pip`   
 To upgrade pip to the latest version run: `pip3 install -U pip`*   
   
##  How to use: server side  
- deploy webhook server `t_webhook.py`  
- set the env var: `export DISCORD_URL=123`  

## How to use: client side  
Note: *The following steps must be performed AFTER the web server has been deployed AND configured!!!*   
- set the env vars:  
`export OAUTH_CLIENT_ID=123`  
`export OAUTH_TOKEN=123`  
  or depending on registration version: `export APP_TOKEN=123`  
`export CALLBACK_URL=http://localhost/`   
`export HUB_SECRET=abc`  
- add the names of the channels you want to, on l_csv_users_str variable at search.py file  
- run search script as: `python3 search.py | tee users.json`  
- run register script as: `python3 register.py`  
   
Note: *To speed up development:*  
- create a new bash script: `touch env_variables.sh`   
- add the script to the .gitignore : `echo "env_variables.sh" >> .gitignore`   
- write all export statements to the `env_variables.sh` script, with the following format:   
    - `export OAUTH_CLIENT_ID="123"`   
    - `export APP_TOKEN="123"`   
    - `export OAUTH_TOKEN="123"`        
    - `export HUB_SECRET="abc"`    
    - `export CALLBACK_URL="http://localhost/"`   
    - `...`   
- run : `source env_variables.sh`   
- on the SAME bash instance run any of the python scripts eg: `python3 search.py`
     
## Debug eventsub webhooks   
To debug eventsub webhooks you can use:   
- the webhook_management script: `python3 webhook_management.py`   
- the twitch-cli:   
  - to test registration verification: `./twitch event verify-subscription streamup --forward-address https://......./eventsub/name/ --secret secretstrhere`   
  - to test notifications : `./twitch event trigger streamup --forward-address https://......./eventsub/name/ --secret secretstrhere`   
  - event types to test: `streamup`, `streamdown`, `raid`
   
Note: *twitch-cli is not available on apt yet, must be cloned from the official Github repo: `/twitchdev/twitch-cli`*   
    
## TODO   
   