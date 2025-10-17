"""
Unit tests for the MiniReviewClient.
"""

import unittest
from unittest.mock import patch

import requests

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    CollectionsOrderBy,
    GameRatingsOrderBy,
    OrderBy,
    Platform,
)
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
            "platforms": [Platform.ANDROID, Platform.IOS],
            "orderBy": OrderBy.MOST_POPULAR,
            "search": None,  # This should be ignored
            "category": "action",  # This should be a string
            "tags": ["2d", "3d"],  # This should be a list of strings
        }

        processed_params = self.client._build_params(params)

        expected_params = {
            "page": 1,
            "limit": 10,
            "platforms[]": ["android", "ios"],
            "orderBy": "most-popular",
            "category": "action",
            "tags[]": ["2d", "3d"],
        }

        self.assertEqual(processed_params, expected_params)

    @patch("minireview_client.client.MiniReviewClient._fetch_api")
    def test_get_filters_caching(self, mock_fetch_api):
        """Test that get_filters caches its response."""
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
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        with self.assertRaises(APIError):
            self.client._fetch_api("/test-endpoint")

    @patch.object(requests.Session, "get")
    def test_fetch_api_http_error(self, mock_get):
        """Test that an APIError is raised on an HTTP error."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found for url: ..."
        )
        mock_get.return_value = mock_response

        with self.assertRaises(APIError) as cm:
            self.client._fetch_api("/test-endpoint")
        self.assertIn("404 Client Error", str(cm.exception))

    @patch("minireview_client.client.MiniReviewClient._fetch_api")
    def test_get_game_ratings_uses_enum(self, mock_fetch_api):
        """Test that get_game_ratings correctly processes its OrderBy enum."""
        self.client.get_game_ratings(
            game_id=123, orderBy=GameRatingsOrderBy.MOST_POPULAR
        )
        call_args, _ = mock_fetch_api.call_args
        self.assertEqual(call_args[0], "/games-ratings")
        self.assertIn("orderBy", call_args[1])
        self.assertEqual(call_args[1]["orderBy"], "most-popular")

    @patch("minireview_client.client.MiniReviewClient._fetch_api")
    def test_get_collections_uses_enum(self, mock_fetch_api):
        """Test that get_collections correctly processes its OrderBy enum."""
        self.client.get_collections(
            orderBy=CollectionsOrderBy.NEWEST,
            is_load_new=True,
            is_load_last_updated=True,
        )
        call_args, _ = mock_fetch_api.call_args
        self.assertEqual(call_args[0], "/collections")
        self.assertIn("orderBy", call_args[1])
        self.assertEqual(call_args[1]["orderBy"], "newest")
        self.assertIn("loadNewcollections", call_args[1])
        self.assertEqual(call_args[1]["loadNewcollections"], 1)
        self.assertIn("loadLastUpdatedcollections", call_args[1])
        self.assertEqual(call_args[1]["loadLastUpdatedcollections"], 1)

    @patch("minireview_client.client.MiniReviewClient.get_filters")
    def test_string_filter_validation(self, mock_get_filters):
        """Test that various string-based filters are validated correctly."""
        mock_get_filters.return_value = [
            {
                "slug": "category",
                "itens": [{"slug": "action"}],
            },
            {
                "slug": "players",
                "itens": [{"slug": "singleplayer"}],
            },
            {
                "slug": "tags",
                "itens": [{"slug": "2d"}],
            },
        ]

        # Test invalid category (single value)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(category="invalid-category")
        self.assertIn("'invalid-category' for filter 'category'", str(cm.exception))

        # Test invalid players (list of values)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(players=["singleplayer", "invalid-player"])
        self.assertIn("'invalid-player' for filter 'players'", str(cm.exception))

        # Test invalid tags (list of values)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(tags=["invalid-tag"])
        self.assertIn("'invalid-tag' for filter 'tags'", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
