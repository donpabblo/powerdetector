from datetime import datetime
import json
import os
import keyring

import pushnotification as push

def detect():
    config_path = os.path.join(os.path.expanduser("~"), ".config", "powerdetector")
    timestamp_format = "%d-%m-%Y %H:%M:%S"
    try:
        with open(os.path.join(config_path, "config.json")) as json_file:
            notification_json = json.load(json_file)
            ifttt_name = notification_json["ifttt_event"]
            current_timestamp = datetime.now()
            current_timestring = datetime.strftime(current_timestamp, timestamp_format)
            api_key = keyring.get_password("IFTTT-OutageDetector", ifttt_name)
            push.push_to_ifttt(ifttt_name, api_key, "Power was ON at: {}".format(current_timestring))
    except FileNotFoundError:
        print("Configuration file does not exist, try running the initial configuration again!")
    except KeyError:
        print("Config.json file doesn't have all fields, try running the initial configuration again!")
    
    print("Script has run at {}".format(current_timestring))

if __name__ == '__main__':
    detect()