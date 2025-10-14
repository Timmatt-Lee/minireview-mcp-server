"""
Unit tests for the MiniReviewClient.
"""

import unittest
from unittest.mock import patch

import requests

from minireview_client.client import MiniReviewClient
from minireview_client.exceptions import APIError


class TestMiniReviewClient(unittest.TestCase):
    """Test suite for the MiniReviewClient."""

    def setUp(self):
        """Set up a new client for each test."""
        self.client = MiniReviewClient()

    @patch("minireview_client.client.requests.Session")
    def test_init(self, mock_session):
        """Test that the client initializes with a session object."""
        client = MiniReviewClient()
        self.assertIsNotNone(client._session)

    def test_build_params(self):
        """Test the _build_params method for correct parameter formatting."""
        params = {
            "page": 1,
            "limit": 10,
            "platforms": ["android", "ios"],
            "orderBy": "most-popular",
            "search": None,  # This should be ignored
        }

        processed_params = self.client._build_params(params)

        expected_params = {
            "page": 1,
            "limit": 10,
            "platforms[]": ["android", "ios"],
            "orderBy": "most-popular",
        }

        self.assertEqual(processed_params, expected_params)

    @patch("minireview_client.client.MiniReviewClient._fetch_api")
    def test_get_filters_caching(self, mock_fetch_api):
        """Test that get_filters caches its response."""
        # This test needs to be adjusted because get_filters now calls get_games_list
        # which in turn calls _fetch_api. So we mock the return value for the
        # get_games_list call.
        mock_response = {
            "filtros": [{"slug": "platforms", "itens": []}],
            "data": [],
        }
        mock_fetch_api.return_value = mock_response

        # First call - should call the API
        filters1 = self.client.get_filters()
        self.assertEqual(mock_fetch_api.call_count, 1)
        self.assertEqual(filters1, mock_response["filtros"])

        # Second call - should use the cache
        filters2 = self.client.get_filters()
        self.assertEqual(mock_fetch_api.call_count, 1)  # Should not have increased
        self.assertEqual(filters2, mock_response["filtros"])

    @patch("minireview_client.client.MiniReviewClient._fetch_api")
    def test_get_game_details_call(self, mock_fetch_api):
        """Test that get_game_details calls _fetch_api with correct params."""
        game_slug = "my-game"
        category = "action"

        self.client.get_game_details(game_slug, category)

        mock_fetch_api.assert_called_once_with(
            f"/games/{game_slug}", {"getBy": "slug", "category": category}
        )

    @patch.object(requests.Session, "get")
    def test_fetch_api_error(self, mock_get):
        """Test that an APIError is raised on a request exception."""
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        with self.assertRaises(APIError):
            self.client._fetch_api("/test-endpoint")

    @patch("minireview_client.client.MiniReviewClient.get_filters")
    def test_validation_raises_error_for_invalid_filter(self, mock_get_filters):
        """Test that _validate_params raises ValueError for an invalid filter value."""
        # Setup the mock to return a predefined set of filters
        mock_get_filters.return_value = [
            {
                "slug": "category",
                "nome": "Category",
                "itens": [{"slug": "action"}, {"slug": "adventure"}],
            }
        ]

        # Call a method that uses validation with an invalid category
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(category="invalid-category")

        # Check if the error message is as expected
        self.assertIn(
            "Invalid value 'invalid-category' for filter 'category'", str(cm.exception)
        )


if __name__ == "__main__":
    unittest.main()
