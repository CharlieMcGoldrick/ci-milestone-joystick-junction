import requests
import logging
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)


def get_twitch_access_token():
    """
    Retrieves an access token from Twitch for API authentication.

    The function sends a POST request to Twitch's OAuth2 token endpoint with
    client credentials.

    On success, it returns the access token; on failure, it logs the error and
    returns None.
    """
    # Twitch OAuth2 token endpoint
    url = 'https://id.twitch.tv/oauth2/token'

    # Payload with client credentials for authentication
    payload = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    try:
        # Make a POST request to obtain the access token
        response = requests.post(url, data=payload)
        # Raise error for HTTP status codes 4xx/5xx
        response.raise_for_status()
        # Extract and return the access token
        return response.json().get('access_token')
    except requests.RequestException as e:
        # Log any request-related exceptions and return None
        logger.error(f"Failed to retrieve access token: {e}")
        return None


def make_igdb_api_request(endpoint, query_body):
    """
    Makes a POST request to the IGDB API using the provided endpoint and query
    body.

    The function first attempts to retrieve a Twitch access token. If
    successful, it constructs a POST request to the specified IGDB API
    endpoint with the necessary headers. On successful response, it returns
    the JSON data; on failure, it logs the error and returns None.
    """
    # Retrieve the access token for authentication
    access_token = get_twitch_access_token()
    if access_token is None:
        # Log and return None if access token is not available
        logger.error("No access token available for IGDB API request.")
        return None

    # Construct the full URL for the IGDB API request
    url = f'https://api.igdb.com/v4/games'

    # Headers including Client-ID and Authorization token
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }

    try:
        # Make the POST request to the IGDB API
        response = requests.post(url, headers=headers, data=query_body)
        # Raise error for HTTP status codes 4xx/5xx
        response.raise_for_status()
        # Return the JSON data from the response
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log any request-related exceptions and return None
        logger.error(f"Error making IGDB API request to {endpoint}: {e}")
        return None
