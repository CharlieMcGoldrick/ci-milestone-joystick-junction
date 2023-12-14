import requests
import logging
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)


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
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raises an error for bad status codes
        return response.json().get('access_token')
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve access token: {e}")
        return None


def make_igdb_api_request(endpoint, query_body):
    """
    This function makes a POST request to the IGDB API using the provided endpoint and query.
    """
    access_token = get_twitch_access_token()
    if access_token is None:
        logger.error("No access token available for IGDB API request.")
        return None

    url = f'https://api.igdb.com/v4/{endpoint}'
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers, data=query_body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making IGDB API request to {endpoint}: {e}")
        return None
