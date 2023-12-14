from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, MagicMock
import requests

# Adjust the import path as necessary
from .api import get_twitch_access_token, make_igdb_api_request


class GetTwitchAccessTokenTests(TestCase):
    def setUp(self):
        self.url = 'https://id.twitch.tv/oauth2/token'
        self.payload = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'client_secret': settings.TWITCH_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }


    @patch('requests.post')
    def test_get_access_token_failure(self, mock_post):
        # Mocking a failure response from the Twitch API
        mock_post.return_value = MagicMock(
            status_code=400, json=MagicMock(return_value={}))

        token = get_twitch_access_token()
        self.assertIsNone(token)

    @patch('requests.post')
    def test_get_access_token_success(self, mock_post):
        # Mocking a successful response from the Twitch API
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        mock_post.return_value = mock_response

        token = get_twitch_access_token()
        self.assertEqual(token, 'test_access_token')


class IGDBAPITests(TestCase):
    def setUp(self):
        self.url = 'https://id.twitch.tv/oauth2/token'
        self.payload = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'client_secret': settings.TWITCH_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

    @patch('requests.post')
    def test_igdb_api_request_failure(self, mock_post):
        # Mocking an unsuccessful response from the IGDB API
        mock_post.return_value = MagicMock(status_code=400)
        # Return an empty dict instead of None
        mock_post.return_value.json.return_value = {}

        response = make_igdb_api_request('games', 'fields *;')
        self.assertIsNone(response)

    @patch('message_board.api.api.get_twitch_access_token')
    @patch('requests.post')
    def test_make_igdb_api_request_success(self, mock_post,
                                           mock_get_access_token):
        # Mock the access token retrieval
        mock_get_access_token.return_value = 'mock_access_token'

        # Set up a mock response object
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'data': 'mock_data'}

        # Mock the post request to return the mock response
        mock_post.return_value = mock_response

        # Define test data
        test_endpoint = 'games'
        test_query_body = 'fields name;'

        # Call the function
        response = make_igdb_api_request(test_endpoint, test_query_body)

        # Assertions
        mock_post.assert_called_once_with(
            f'https://api.igdb.com/v4/{test_endpoint}',
            headers={
                'Client-ID': settings.TWITCH_CLIENT_ID,
                'Authorization': f'Bearer mock_access_token'
            },
            data=test_query_body
        )
        self.assertEqual(response, {'data': 'mock_data'})
