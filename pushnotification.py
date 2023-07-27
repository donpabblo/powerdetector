import requests

def push_to_ifttt(ifttt_name, api_key, notification):
    requests.post(url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(ifttt_name, api_key), data = {'value1':notification})