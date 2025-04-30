# ngrok-for-testing-telegram-bot

### What is this script
To develop/test a Telegram bot you need to set a Webhook (by the API) that point to a file on the web.
So you can't develop a Telegram bot locally, unless you safely publish your local folder to the web.
[**ngrok**](https://ngrok.com/) allows you to make available your localhost on the web. Putting your localhost on the web, ngrok provides you the created domain and, by that domain, you can create the Telegram bot webhook. This script simply allows you to automate the process of creating the ngrok tunnel and deleting the webhook to create the new one every time you start ngrok.

Article about it [here](https://giuseppetrivi.github.io/posts/testare-bot-telegram-in-locale-con-ngrok/) (in italian, translate it via browser translation).

---
### Prerequisites to start the script
This are all the (easy and common) prerequisites to start the script:
- Create a base Telegram bot ([tutorial here](https://core.telegram.org/bots/tutorial))
- Clone locally the repository (`git clone LINK_TO_THIS_REPO`)
- [Download Python](https://www.python.org/downloads/)
- [Register to ngrok](https://dashboard.ngrok.com/signup)
- [Download ngrok](https://ngrok.com/download) (step 1 and 2 [here](https://ngrok.com/docs/getting-started/))
- [Download Python library "pyngrok"](https://pypi.org/project/pyngrok/)
- Download a local server (like [XAMPP](https://www.apachefriends.org/it/index.html))

---
### How it works
After fulfilling the above prerequisites, you need to place the `ngrok.yml` file in the ngrok configuration folder, which may vary depending on the OS on which it is installed ([info here](https://ngrok.com/docs/agent/config/)). Then you need to insert the path to the file on line 47 of `auto_ngrok.py`:
```py
...
ngrok_config_file_path = "Here/The/Path/ngrok.yml" 
...
```

Now you can use this script, executing it into the command line:
```sh
py auto_ngrok.py ...
```

The script accepts the following arguments on the command line:
- `-f LOCAL_FOLDER_PATH`: the location of the file which serves as webhook access point; this file has to be in the localhost folder (for XAMPP is "`.../xampp/htdocs/`", for example)
- `-t TELEGRAM_BOT_TOKEN`: the Telegram Bot API token
- `-c CUSTOM_CONFIG_FILE`: a custom configuration file to easily start scripts

If you use a `-c`, the other parameters will be taken from the configuration file. Otherwise yu need to specify `-f` and `-t`.

### Configuration file
You can create custom configuration files with the following structure:
```json
{
  "ngrok_config_file_path": "C:/path/to/ngrok/config/folder/ngrok.yml",
  "local_folder_path": "/crypto_bot_project/index.php",
  "telegram_bot_token": "238423979837589fwe8ydys7s7tyr78"
}
```

And then use it:
```sh
py auto_ngrok.py -c crypto_bot_config
```

