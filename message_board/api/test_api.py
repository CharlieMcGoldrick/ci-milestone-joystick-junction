from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, MagicMock
import requests

from .api import get_twitch_access_token, make_igdb_api_request


class BaseAPITestCase(TestCase):
    """
    Base class for API test cases.

    This class provides common setup for testing API related functions.
    It also includes a helper method to configure mock responses for requests.
    """

    def setUp(self):
        """
        Common setup for all API tests, initializing mock response and common
        payload.
        """
        self.mock_response = MagicMock()
        self.url = 'https://id.twitch.tv/oauth2/token'
        self.payload = {
            'client_id': settings.TWITCH_CLIENT_ID,
            'client_secret': settings.TWITCH_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

    def configure_mock_response(self, mock_post, status_code, json_data):
        """
        Configures the mock response for `requests.post` with given status
        code and json data.

        Args:
            mock_post (MagicMock): The mock object for requests.post.
            status_code (int): The HTTP status code to simulate.
            json_data (dict): The JSON data to return in the response.
        """
        self.mock_response.status_code = status_code
        self.mock_response.json.return_value = json_data
        mock_post.return_value = self.mock_response


class GetTwitchAccessTokenTests(BaseAPITestCase):
    """
    Test cases for the get_twitch_access_token function.
    """

    @patch('requests.post')
    def test_access_token_retrieval_fails(self, mock_post):
        """
        Test to ensure proper handling of failed access token retrieval.
        """
        self.configure_mock_response(mock_post, 400, {})
        token = get_twitch_access_token()
        self.assertIsNone(token)

    @patch('requests.post')
    def test_access_token_retrieval_succeeds(self, mock_post):
        """
        Test to ensure access token is successfully retrieved when Twitch AP
        responds correctly.
        """
        self.configure_mock_response(
            mock_post, 200, {'access_token': 'test_access_token'})
        token = get_twitch_access_token()
        self.assertEqual(token, 'test_access_token')


class IGDBAPITests(BaseAPITestCase):
    """
    Test cases for the make_igdb_api_request function.
    """

    @patch('requests.post')
    def test_igdb_api_request_fails(self, mock_post):
        """
        Test to ensure that the IGDB API request correctly handles failure
        scenarios.
        """
        self.configure_mock_response(mock_post, 400, {})
        response = make_igdb_api_request('games', 'fields *;')
        self.assertIsNone(response)

    @patch('message_board.api.api.get_twitch_access_token')
    @patch('requests.post')
    def test_igdb_api_request_succeeds(self, mock_post, mock_get_access_token):
        """
        Test to verify successful IGDB API requests and correct data handling.
        """
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
