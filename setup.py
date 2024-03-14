import os
import sys

import json
import keyring
import getpass

import requests
import cron_scheduling
import pushnotification as push

def curate_input(shown_message, expected_values):
    result = input(shown_message)
    if result in expected_values:
        return result.lower()
    else:
        return curate_input("You need to input one of the following: {}. Try again! ".format(expected_values),
                            expected_values)
    
def initialize(notification_type):
    config_path = os.path.join(os.path.expanduser("~"), ".config","powerdetector")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    
    config = {}
    it_worked = False
    failed_attempts = 0

    while not it_worked:
        if (notification_type == 'ifttt'):
            try:
                ifttt_name = input("Input your IFTTT event name: ")
                keyring.set_password("IFTTT-OutageDetector", ifttt_name, getpass.getpass("Input your IFTTT API key: "))
                api_key = keyring.get_password("IFTTT-OutageDetector", ifttt_name)
                print("Trying to send a notification through IFTTT!")
                push.push_to_ifttt(ifttt_name, api_key, "Testing IFTTT")
                it_works = curate_input("Did you get the notification? (y/n) ", ("y", "n"))
                if it_works == "y":
                    it_worked = True
                else:
                    failed_attempts += 1
                    if failed_attempts >= 3:
                        print("Too many failed attempts, exiting script, try again later!")
                        exit(1)
                    print("Check to make sure you followed the steps correctly and try again.")
            except requests.exceptions.ConnectionError:
                print("No internet, try reconnecting and running the script again!")
                exit(1)
            config["type"] = 'ifttt'
            config["ifttt_event"] = ifttt_name
        else:
            try:
                config["type"] = 'google_sheet'
                sheet_url = input("Input your Google sheet url: ")
                config['sheet_url'] = sheet_url
                keyring.set_password("GoogleSheet-OutageDetector", 'secret', getpass.getpass("Input your Google Sheet secret: "))
                secret = keyring.get_password("GoogleSheet-OutageDetector", 'secret')
                print("Trying to send a notification through Google Sheet!")
                push.push_to_google_sheet(sheet_url, secret, "Testing IFTTT", "Testing IFTTT")
                it_works = curate_input("Did you get the notification? (y/n) ", ("y", "n"))
                if it_works == "y":
                    it_worked = True
                else:
                    failed_attempts += 1
                    if failed_attempts >= 3:
                        print("Too many failed attempts, exiting script, try again later!")
                        exit(1)
                    print("Check to make sure you followed the steps correctly and try again.")
            except requests.exceptions.ConnectionError:
                print("No internet, try reconnecting and running the script again!")
                exit(1)

    with open(os.path.join(config_path, 'config.json'), 'w+') as json_file:
            json.dump(config, json_file)

    crontab_edit = curate_input("Would you like to setup the script to run automatically "
                                "(it will run at boot time and at 5 minute intervals)? (y/n)", ("y", "n"))
    if crontab_edit == "y":
        exec_path = os.path.join(os.getcwd(), "power_detector.py")
        cron_scheduling.schedule_job(exec_path, config_path, 30)

if __name__ == '__main__':
    initialize(sys.argv)