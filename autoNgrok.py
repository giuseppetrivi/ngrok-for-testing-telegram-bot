from pyngrok import conf, ngrok
from Webhook import Webhook
import json
import sys
import re


localFolderUri = None
tgBotApiToken = None

# Check the arguments of the script:
# - #1 argument must be the URI of the local file to set as Telegram bot webhook
# - #2 argument must be the Telegram BOT token
scriptArguments = sys.argv
firstArgument = scriptArguments[1] if (1 < len(scriptArguments)) else None
secondArgument = scriptArguments[2] if (2 < len(scriptArguments)) else None

regexToMatchFolderUri = r".+(?=[\\/])[\\/].*(\.)[a-z]*"

if (firstArgument!=None and (firstArgument=="-h" or firstArgument=="--help")):
  print("COMMAND FOR NORMAL EXECUTION IS THIS: autoNgrok.py [path] [(OPTIONAL) telegram bot token]")
  print("COMMAND FOR HELP IS THIS: autoNgrok.py [-h or --help]")
  exit(1)
elif (firstArgument!=None and re.match(regexToMatchFolderUri, firstArgument)):
  localFolderUri = firstArgument
  if (secondArgument!=None and len(secondArgument)==46):
    tgBotApiToken = secondArgument
else:
  print("[!! ERROR]: You should specify the path ending with a file.")
  exit(1)


# Set path of .yml configuration file
conf.get_default().config_path = "" # CHANGE WITH YOUR PATH

ngrokCreatedTunnel = ngrok.connect()
if (ngrokCreatedTunnel is None):
  print("[!! ERROR]: Something wrong during the creation of ngrok tunnel.")
  exit(1)

ngrokPublicUrl = ngrokCreatedTunnel.public_url
protocol = ngrokCreatedTunnel.proto
name = ngrokCreatedTunnel.name
config = ngrokCreatedTunnel.config

# Handle the webhook
webhook = Webhook(tgBotApiToken)
if (not webhook.isUrlValid(ngrokPublicUrl)):
  print("[!! ERROR]: ngrok URL is not valid.")
  exit(1)


ngrokPublicUrlComplete = ngrokPublicUrl + localFolderUri

# Operations to reset the webhook: delete the pre-existent, setting the new one and getting info of the new one)
# Deleting the pre-existent webhook
dwInfo = webhook.deleteWebhook()
if (dwInfo):
  print("## Delete webhook informations ##")
  print(json.dumps(dwInfo, indent=2))
else:
  print("[!! ERROR]: Something wrong while deleting the webhook.")
  exit(1)

print(ngrokPublicUrlComplete)
# Setting the new one (with ngrok public url)
swInfo = webhook.setWebhook(ngrokPublicUrlComplete)
if (swInfo):
  print("## Set new webhook ##")
  print(json.dumps(swInfo, indent=2))
else:
  print("[!! ERROR]: Something wrong while setting the new webhook.")
  exit(1)

# Getting info of new webhook created
infoWebhook = webhook.getWebhookInfo()
if (infoWebhook):
  print("## Get new webhook informations ##")
  print(json.dumps(infoWebhook, indent=2))
else:
  print("[!! ERROR]: Something wrong while getting the new webhook info.")
  exit(1)


# Print info about ngrok tunnel
print()
print("Info about the ngrok tunnel\n")
print(f"\tPublic URL: {ngrokPublicUrl}")
print(f"\tProtocol: {protocol}")
print(f"\tTunnel name: {name}")
print(f"\tTunnel configuration: \n{json.dumps(config, indent=9)}")
print()

# ngrok process
ngrok_process = ngrok.get_ngrok_process()
print("!! Remind to activate your localhost server (XAMPP or whatelse) !!")
print("Press CTRL+C to stop ngrok tunneling")
try:
  # Block until CTRL-C or some other terminating event
  ngrok_process.proc.wait()
except KeyboardInterrupt:
  print("Closing ngrok tunnel ...")
  ngrok.kill()