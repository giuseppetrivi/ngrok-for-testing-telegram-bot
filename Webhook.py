import re
import requests
import json


# Class to handle the requests to the webhook
class Webhook:

  # Fill this var with a default Telegram bot token
  tgBotApiToken = None # CHANGE WITH YOUR DEFAULT TELEGRAM BOT TOKEN

  def __init__(self, tgBotApiToken=None):
    if (tgBotApiToken!=None and len(tgBotApiToken)==46):
      self.tgBotApiToken = tgBotApiToken
    elif (tgBotApiToken==None):
      print("[!! ERROR]: You should specify a Telegram bot token.")
      exit(1)
    pass

  # Method to make different requests to Telegram bot API
  def makeRequestToApi(self, methodName, params=None):
    url = "https://api.telegram.org/bot" + self.tgBotApiToken + "/" + methodName
    request = requests.get(url, params)
    return request

  # Check if a ngrok URL is valid
  def isUrlValid(self, ngrokPublicUrl):
    regex = r"https:\/\/[a-zA-Z0-9-]*.ngrok-free.app"
    if (re.match(regex, ngrokPublicUrl)):
      return True
    else:
      return False
  

  def deleteWebhook(self):
    methodName = "deleteWebhook"
    request = self.makeRequestToApi(methodName)
    if (request.status_code!=200):
      return False
    return json.loads(request.content)
  
  def setWebhook(self, ngrokPublicUrlComplete):
    methodName = "setWebhook"
    params = {
      'url': ngrokPublicUrlComplete
    }
    request = self.makeRequestToApi(methodName, params)
    if (request.status_code!=200):
      return False
    return json.loads(request.content)
  
  def getWebhookInfo(self):
    methodName = "getWebhookInfo"
    request = self.makeRequestToApi(methodName)
    if (request.status_code!=200):
      return False
    return json.loads(request.content)
