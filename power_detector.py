from datetime import datetime
import json
import os
import keyring

import pushnotification as push

def getTime():
    timestamp_format = "%d-%m-%Y %H:%M:%S"
    current_timestamp = datetime.now()
    current_timestring = datetime.strftime(current_timestamp, timestamp_format)
    return current_timestring

def checkOutage(current_timestring):
    config_path = os.path.join(os.path.expanduser("~"), ".config", "powerdetector")
    try:
        with open(os.path.join(config_path, "last_timestamp.txt"), 'r') as last_tmst_file:
            last_tmst = last_tmst_file.readline()
            last_tmst_object = datetime.strptime(last_tmst, '%d-%m-%Y %H:%M:%S')
            difference = last_tmst_object - current_timestring
            outage_in_minutes = difference.total_seconds() / 60
            if outage_in_minutes > 59:
                return outage_in_minutes
            else:
                return None
    except FileNotFoundError:
        print("last_timestamp file does not exist! Creating it!")
        with open(os.path.join(config_path, "last_timestamp.txt"), 'w') as f:
            f.write(current_timestring)
        return None
    except:
        print("Error!")

def detect():
    try:
        config_path = os.path.join(os.path.expanduser("~"), ".config", "powerdetector")
        current_timestring = getTime()
        outage = checkOutage(current_timestring)
        with open(os.path.join(config_path, "config.json")) as json_file:
            notification_json = json.load(json_file)
            type = notification_json["type"]
            if type == 'ifttt':
                ifttt_name = notification_json["ifttt_event"]
                api_key = keyring.get_password("IFTTT-OutageDetector", ifttt_name)
                push.push_to_ifttt(ifttt_name, api_key, "Power was ON at: {}".format(current_timestring))
            else:
                sheet_url = notification_json["sheet_url"]
                secret = keyring.get_password("GoogleSheet-OutageDetector", 'secret')
                push.push_to_google_sheet(sheet_url, secret, current_timestring, "Power was ON at: {}".format(current_timestring))
                if outage:
                    push.push_to_google_sheet(sheet_url, secret, current_timestring, "Power was OUT for: {} minutes".format(outage), outage)
    except FileNotFoundError:
        print("Configuration file does not exist, try running the initial configuration again!")
    except KeyError:
        print("Config.json file doesn't have all fields, try running the initial configuration again!")
    
    print("Script has run at {}".format(current_timestring))

if __name__ == '__main__':
    detect()