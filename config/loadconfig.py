import sys
import json

try:
    with open('config/config.json', 'r') as f:
        config = json.load(f)
        ignored = config["ignore_extensions"]
        prefixes = config["prefixes"]
        game = config["default_game"]
        my_id = int(config["owner_id"])
except(FileNotFoundError):
    print("Couldn't open config file. Exiting")
    sys.exit()

try:
    with open('config/keys.json', 'r') as f:
        keys = json.load(f)
        token = keys["token"]
        bitly_token = keys["bitly_token"]
except(FileNotFoundError):
    print("Couldn't open keys file. Exiting")
    sys.exit()
