import sys
import json
import logging as log

try:
    with open('config/config.json', 'r') as f:
        config = json.load(f)
        ignored = config["ignore_extensions"]
        prefixes = config["prefixes"]
        game = config["default_game"]
        my_id = int(config["owner_id"])
        banned_words = config["banned_words"]
        repo_list = config["repo_list"]
except(FileNotFoundError):
    log.fatal("Couldn't open config file. Exiting")
    sys.exit()

try:
    with open('config/keys.json', 'r') as f:
        keys = json.load(f)
        token = keys["token"]
        bitly_token = keys["bitly_token"]
        google_api_key = keys["google_api_key"]
        custom_search_engine = keys["custom_search_engine"]
except(FileNotFoundError):
    log.fatal("Couldn't open keys file. Exiting")
    sys.exit()
