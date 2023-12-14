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
