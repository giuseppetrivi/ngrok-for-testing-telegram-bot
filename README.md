# ngrok-for-testing-telegram-bot
### Pre-requisites to start the script
- [Download Python](https://www.python.org/downloads/)
- [Download ngrok](https://ngrok.com/download) and register to it
- [Download Python library "pyngrok"](https://pypi.org/project/pyngrok/)
- Put the file ngrok.yml into the ngrok's configuration folder ([depends on the OS](https://ngrok.com/docs/agent/config/)) and write the path of the file into `autoNgrok.py`
- Download a local server (like [XAMPP](https://www.apachefriends.org/it/index.html))

---
### What is this?
To develop/test a Telegram bot you need to set a Webhook (by the API) that point to a local file on the web.
So you can't develop a Telegram bot locally, unless ...

Unless you put your local project folder on the web.
**ngrok** allows you to put your localhost on the web (visit ngrok website or blogs if you want details and safety guarantee).
Putting your localhost on the web, ngrok provides you the created domain and, by that domain, you can create the Telegram bot webhook.

This script simply allows you to automate the process of creating the ngrok tunnel and deleting the webhook to create the new one, everytime you start ngrok.

### How does it work?
The script accept 2 arguments on the command line:
- the location of the file which serves as webhook access point, that has to be in the localhost folder (for XAMPP is "`.../xampp/htdocs/`", for example)
- the Telegram bot API token. You can also hardcode it into `Webhook.py` class, if you don't want to pass it everytime as an argument.

