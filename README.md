# 🤖 ngrok-for-testing-telegram-bot

## What is this script
To develop or test a Telegram bot, you need to set a Webhook (via the Telegram API) that points to a publicly accessible file on the web.  
This means you can't develop a Telegram bot locally unless you expose your local folder to the web securely.

[**ngrok**](https://ngrok.com/) allows you to expose your localhost to the internet. It provides a temporary public domain pointing to your local server, which you can use to set up your bot's Webhook.  
This script automates the process of creating an ngrok tunnel and updating the Telegram Webhook accordingly each time ngrok is started.

Related article (in Italian) [here](https://giuseppetrivi.github.io/posts/testare-bot-telegram-in-locale-con-ngrok/) (use browser translation if needed).

---
## What to do

### Prerequisites
These are all the (easy and common) prerequisites to run the script:

- Create a base Telegram bot ([tutorial here](https://core.telegram.org/bots/tutorial))
- Clone this repository locally (`git clone LINK_TO_THIS_REPO`)
- [Install Python](https://www.python.org/downloads/)
- [Register for ngrok](https://dashboard.ngrok.com/signup)
- [Download ngrok](https://ngrok.com/download) (see steps 1 and 2 [here](https://ngrok.com/docs/getting-started/))
- [Install the `pyngrok` Python library](https://pypi.org/project/pyngrok/)
- Install a local server (like [XAMPP](https://www.apachefriends.org/it/index.html))

---
### Setup
Once the prerequisites are met, place the `ngrok.yml` configuration file in the ngrok config folder (its location depends on your OS — [more info here](https://ngrok.com/docs/agent/config/)). You need also to put your authtoken into this file (you can find it into your ngrok account, under "Your Authtoken" in the menu):

```yml
authtoken: <YOUR NGROK AUTH TOKEN>
```

Then, specify the path to that config file on line 47 of `auto_ngrok.py`:
```py
...
ngrok_config_file_path = "/Here/The/Path/ngrok.yml"
...
```

Now you can run the script from the command line:
```sh
py auto_ngrok.py ...
```

### Arguments
The script accepts the following command-line arguments:
- `-f LOCAL_FOLDER_PATH`: the path to the file that acts as the Webhook endpoint. This file must be within your localhost folder (for example, in XAMPP, it's `.../xampp/htdocs/`)
- `-t TELEGRAM_BOT_TOKEN`: your Telegram Bot API token
- `-c CUSTOM_CONFIG_FILE`: name of a custom configuration file to easily reuse settings

If you use `-c`, the other parameters (`-f` and `-t`) will be read from the configuration file. Otherwise, they must be specified manually.

### Configuration file
You can create custom configuration files with the following structure (for example `crypto_bot_config.json`):
```json
{
  "ngrok_config_file_path": "C:/path/to/ngrok/config/folder/ngrok.yml",
  "local_folder_path": "/crypto_bot_project/index.php",
  "telegram_bot_token": "238423979837589fwe8ydys7s7tyr78"
}
```
Then, run the script like this:
```sh
py auto_ngrok.py -c crypto_bot_config
```

---
### Optional: run the script globally from the terminal
By default, you need to refer to the full script path every time (e.g. `C:\Users\username\Desktop\ngrok-for-testing-telegram-bot\`).
To avoid this, you can make it callable globally depending on your OS. Below are two ways to do that in Linux and Windows (other alternatives exist).

#### Linux
You can remove the `.py` to `auto_ngrok.py`, then make the script executable:
```sh
chmod +x auto_ngrok
```
Then, create a symbolic link to the script:
```sh
ln -s ~/original/path/auto_ngrok ~/.local/bin/auto_ngrok
```
The `~/.local/bin` folder is usually included in your system’s PATH.


#### Windows
In Windows, add the script folder (e.g. `C:\Users\username\Desktop\ngrok-for-testing-telegram-bot\`) to the system's Path environment variable.
Then create a batch file `ngrok-bot-start.bat` as follows:
```bat
@echo off
set script_dir=%~dp0
py "%script_dir%auto_ngrok.py" %*
pause
```
This allows you to run `ngrok-bot-start` from anywhere in the terminal.
