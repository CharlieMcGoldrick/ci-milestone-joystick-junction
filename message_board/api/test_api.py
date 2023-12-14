from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, MagicMock
import requests

from .api import get_twitch_access_token, make_igdb_api_request

# Base test class for shared setup
class BaseAPITestCase(TestCase):
    def setUp(self):
        # Common setup for all API tests
        self.mock_response = MagicMock()
        self.url = 'https://id.twitch.tv/oauth2/token'
        self.payload = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'client_secret': settings.TWITCH_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

    def configure_mock_response(self, mock_post, status_code, json_data):
        # Configures the mock response for `requests.post`
        self.mock_response.status_code = status_code
        self.mock_response.json.return_value = json_data
        mock_post.return_value = self.mock_response

# Test class for get_twitch_access_token function
class GetTwitchAccessTokenTests(BaseAPITestCase):

    @patch('requests.post')
    def test_access_token_retrieval_fails(self, mock_post):
        # Test case for failure in retrieving the Twitch access token
        self.configure_mock_response(mock_post, 400, {})
        token = get_twitch_access_token()
        self.assertIsNone(token)

    @patch('requests.post')
    def test_access_token_retrieval_succeeds(self, mock_post):
        # Test case for successful retrieval of the Twitch access token
        self.configure_mock_response(
            mock_post, 200, {'access_token': 'test_access_token'})
        token = get_twitch_access_token()
        self.assertEqual(token, 'test_access_token')

# Test class for make_igdb_api_request function
class IGDBAPITests(BaseAPITestCase):

    @patch('requests.post')
    def test_igdb_api_request_fails(self, mock_post):
        # Test case for failure in IGDB API request
        self.configure_mock_response(mock_post, 400, {})
        response = make_igdb_api_request('games', 'fields *;')
        self.assertIsNone(response)

    @patch('message_board.api.api.get_twitch_access_token')
    @patch('requests.post')
    def test_igdb_api_request_succeeds(self, mock_post, mock_get_access_token):
        # Test case for successful IGDB API request
        mock_get_access_token.return_value = 'mock_access_token'
        self.configure_mock_response(mock_post, 200, {'data': 'mock_data'})

        response = make_igdb_api_request('games', 'fields name;')
        self.assertEqual(response, {'data': 'mock_data'})
        mock_post.assert_called_once_with(
            f'https://api.igdb.com/v4/games',
            headers={
                'Client-ID': settings.TWITCH_CLIENT_ID,
                'Authorization': f'Bearer mock_access_token'
            },
            data='fields name;'
        )
