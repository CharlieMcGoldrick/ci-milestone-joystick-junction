import requests
from django.conf import settings


def get_twitch_access_token():
    """
    This function retrieves an access token from Twitch for API authentication.
    """
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


def make_igdb_api_request(endpoint, query_body):
    """
    This function makes a POST request to the IGDB API using the provided endpoint and query.
    """
    access_token = get_twitch_access_token()
    if access_token is None:
        return None  # or handle the error as needed

    url = f'https://api.igdb.com/v4/{endpoint}'  # Construct the full URL
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=query_body)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors (such as logging them, raising exceptions, etc.)
        return None
