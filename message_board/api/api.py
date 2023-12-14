import requests
from django.conf import settings


def get_twitch_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
        