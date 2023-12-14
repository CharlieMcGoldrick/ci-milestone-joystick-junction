from django.test import TestCase
from django.conf import settings
from unittest.mock import patch
import requests

# Adjust the import path as necessary
from .api import get_twitch_access_token


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
        mock_post.return_value.status_code = 400

        token = get_twitch_access_token()
        self.assertIsNone(token)

    @patch('requests.post')
    def test_get_access_token_success(self, mock_post):
        # Mocking a successful response from the Twitch API
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_access_token'}

        token = get_twitch_access_token()
        self.assertEqual(token, 'test_access_token')
