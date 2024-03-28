import requests

def push_to_ifttt(ifttt_name, api_key, notification):
    requests.post(url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(ifttt_name, api_key), data = {'value1':notification})

def push_to_google_sheet(url, secret, tmst, msg, outage = None):
    if outage:
        sheet_url = url + '?secret={}&tmst={}&msg={}&outage=true'
    else:
        sheet_url = url + '?secret={}&tmst={}&msg={}'
    requests.get(url = sheet_url.format(secret, tmst, msg))
    

        