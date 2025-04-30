import re
import requests
import json


# Class to handle the requests to the webhook
class Webhook:


  telegram_bot_token = None


  @staticmethod
  # Function to check the validity of a Telegram bot token
  def isBotTokenValid(token):
    if (token==None):
      return False
    
    if (not len(token)==46):
      return False
    return True


  def __init__(self, telegram_bot_token=None):
    if (Webhook.isBotTokenValid(telegram_bot_token)):
      self.telegram_bot_token = telegram_bot_token
    else:
      print("[ERROR]: Telegram bot token not valid.")
      exit(1)
    pass

  # Method to make different requests to Telegram bot API
  def makeRequestToApi(self, method_name, params=None):
    url = "https://api.telegram.org/bot" + self.telegram_bot_token + "/" + method_name
    request = requests.get(url, params)
    return request

  # Check if a ngrok URL is valid
  def isUrlValid(self, ngrok_public_url):
    regex = r"https:\/\/[a-zA-Z0-9-]*.ngrok-free.app"
    if (re.match(regex, ngrok_public_url)):
      return True
    else:
      return False
  
  # Methods to handle webhook
  def deleteWebhook(self):
    method_name = "deleteWebhook"
    request = self.makeRequestToApi(method_name)
    if (request.status_code!=200):
      return False
    return json.loads(request.content)
  
  def setWebhook(self, ngrok_public_url_complete):
    method_name = "setWebhook"
    params = {
      'url': ngrok_public_url_complete
    }
    request = self.makeRequestToApi(method_name, params)
    if (request.status_code!=200):
      return False
    return json.loads(request.content)
  
  def getWebhookInfo(self):
    method_name = "getWebhookInfo"
    request = self.makeRequestToApi(method_name)
    if (request.status_code!=200):
      return False
    return json.loads(request.content)
