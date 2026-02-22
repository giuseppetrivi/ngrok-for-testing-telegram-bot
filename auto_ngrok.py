#!/usr/bin/env python3
from pyngrok import conf, ngrok
from Webhook import Webhook
from pathlib import Path
import argparse
import json
import sys
import re


divisor_length = 70

def print_error(message):
  print("❌ [ERROR]: {message}")


# Function to check the validity of a path
def isPathValid(str_path):
  if (str_path==None):
    return False
  
  regexToMatchFolderUri = r".+(?=[\\/])[\\/].*(\.)[a-z]*"
  if (not re.match(regexToMatchFolderUri, str_path)):
    return False
  return True


####################################



# Parsing arguments
parser = argparse.ArgumentParser(
  usage="Use -c CUSTOM_CONFIG_FILE alone or use -f LOCAL_FOLDER_PATH -t TELEGRAM_BOT_TOKEN. If you use all arguments, -c CUSTOM_CONFIG_FILE will prevale.",
  description="Script to handle local develop/test of a Telegram bot."
)

parser.add_argument('-f', '--local_folder_path', type=str, help="(string) Path of local folder with Telegram bot code")
parser.add_argument('-t', '--telegram_bot_token', type=str, help="(string) Telegram bot token [from @BotFather]")
parser.add_argument('-c', '--custom_config_file', type=str, help="(string) Name of custom configuration to execute the script")

args = parser.parse_args()

ngrok_config_file_path = None   # Change this with the default folder path of ngrok.yml file

local_folder_path = args.local_folder_path
telegram_bot_token = args.telegram_bot_token
custom_config_file = args.custom_config_file


# Checking arguments
if (custom_config_file != None):
  script_path = Path(__file__).resolve().parent
  config_filepath = script_path / "config_files" / (custom_config_file + ".json")
  with open(config_filepath, 'r') as file:
    config_data = json.load(file)

  ngrok_config_file_path = config_data["ngrok_config_file_path"]
  local_folder_path = config_data["local_folder_path"]
  telegram_bot_token = config_data["telegram_bot_token"]

  if (not isPathValid(ngrok_config_file_path) or not isPathValid(local_folder_path) or not Webhook.isBotTokenValid(telegram_bot_token)):
    print_error("Something wrong in the definition of properties in custom config file")
    exit(1)
else:
  if (not isPathValid(local_folder_path) or not Webhook.isBotTokenValid(telegram_bot_token)):
    print_error("Something wrong in the definition of arguments. Valid combinations" \
    " of arguments are \"-c ..\" and \"-f .. -t ..\"")
    exit(1)



# Set path of .yml configuration file
conf.get_default().config_path = ngrok_config_file_path

# Create ngrok tunnel
ngrok_created_tunnel = ngrok.connect()
if (ngrok_created_tunnel is None):
  print_error("Something wrong during the creation of ngrok tunnel.")
  exit(1)

# Info from created ngrok tunnel
ngrok_public_url = ngrok_created_tunnel.public_url
protocol = ngrok_created_tunnel.proto
name = ngrok_created_tunnel.name
config = ngrok_created_tunnel.config

## Handle the webhook (operations to reset the webhook: delete the pre-existent, setting the new one and getting info of the new one)
webhook = Webhook(telegram_bot_token)
if (not webhook.isUrlValid(ngrok_public_url)):
  print_error("ngrok URL is not valid.")
  exit(1)

ngrok_public_url_for_webhook = ngrok_public_url + local_folder_path
print("ngrok URL: ", ngrok_public_url_for_webhook)

# Deleting the pre-existent webhook
delete_webhook_info = webhook.deleteWebhook()
if (delete_webhook_info):
  print("\n" + "="*divisor_length)
  print(f"{'ℹ️ Delete webhook info':^60}")
  print("="*divisor_length)
  print(json.dumps(delete_webhook_info, indent=2))
else:
  print_error("Something wrong while deleting the webhook.")
  exit(1)

# Setting the new webhook (with ngrok public url)
set_webhook_info = webhook.setWebhook(ngrok_public_url_for_webhook)
if (set_webhook_info):
  print("\n" + "="*divisor_length)
  print(f"{'ℹ️ Set webhook info':^60}")
  print("="*divisor_length)
  print(json.dumps(set_webhook_info, indent=2))
else:
  print_error("Something wrong while setting the new webhook.")
  exit(1)

# Getting info of new webhook created
general_webhook_info = webhook.getWebhookInfo()
if (general_webhook_info):
  print("\n" + "="*divisor_length)
  print(f"{'ℹ️ General webhook info':^60}")
  print("="*divisor_length)
  print(json.dumps(general_webhook_info, indent=2))
else:
  print_error("Something wrong while getting the new webhook info.")
  exit(1)

# Print info about ngrok tunnel
print("\n" + "="*divisor_length)
print(f"{'🔗 Info ngrok tunnel':^60}")
print("="*70)
print(f"  Public URL:        {ngrok_public_url}")
print(f"  Protocol:          {protocol}")
print(f"  Tunnel name:       {name}")
print(f"  Configuration:     {json.dumps(config)}")
print(f"  Inspect requests:  http://localhost:4040/inspect/http")
print("="*divisor_length)

# ngrok process
ngrok_process = ngrok.get_ngrok_process()
print("\n⚠️  Remind to activate your localhost server (XAMPP or whatelse)!")
print("Press CTRL+C to stop ngrok tunneling")
try:
  # Block until CTRL-C or some other terminating event
  ngrok_process.proc.wait()
except KeyboardInterrupt:
  print("Closing ngrok tunnel ...")
  ngrok.kill()