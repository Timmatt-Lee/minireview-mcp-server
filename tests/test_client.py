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
            game_id=123, orderBy=GameRatingsOrderBy.MOST_RELEVANT, type="all"
        )
        call_args, _ = mock_fetch_api.call_args
        self.assertEqual(call_args[0], "/games-ratings")
        self.assertIn("orderBy", call_args[1])
        self.assertEqual(call_args[1]["orderBy"], "most-relevant")
        self.assertIn("type", call_args[1])
        self.assertEqual(call_args[1]["type"], "all")

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
        self.assertIn(
            "Invalid value for filter 'category': 'invalid-category'", str(cm.exception)
        )

        # Test invalid players (list of values)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(players=["singleplayer", "invalid-player"])
        self.assertIn(
            "Invalid value for filter 'players': 'invalid-player'", str(cm.exception)
        )

        # Test invalid tags (list of values)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(tags=["invalid-tag"])
        self.assertIn(
            "Invalid value for filter 'tags': 'invalid-tag'", str(cm.exception)
        )

    @patch("minireview_client.client.MiniReviewClient._fetch_api")
    def test_get_special_top_games(self, mock_fetch_api):
        """Test that get_special_top_games calls _fetch_api with correct params."""
        slug = "my-slug"
        self.client.get_special_top_games(slug)
        mock_fetch_api.assert_called_once_with(f"/special-top-games/{slug}")


@patch("minireview_client.client.MiniReviewClient._fetch_api", return_value=True)
class TestParameterValidation(unittest.TestCase):
    """A test suite for all parameter validation in the client."""

    def setUp(self):
        """Set up a new client and mock get_filters for each test."""
        self.client = MiniReviewClient()
        self.mock_filters = {
            "platforms": {"android", "ios"},
            "players": {"singleplayer", "multiplayer"},
            "network": {"online", "offline"},
            "monetization-android": {"free", "paid"},
            "monetization-ios": {"free", "paid"},
            "screen-orientation": {"portrait", "landscape"},
            "category": {"action", "adventure"},
            "sub-category": {"rpg", "sandbox"},
            "tags": {"2d", "3d", "pixel-art"},
            "countries-android": {"us", "br"},
            "countries-ios": {"us", "ca"},
            "score": {"gameplay", "control"},
        }
        self.client._parsed_filters = self.mock_filters

    def test_get_games_list_score_validation(self, mock_fetch):
        """Test get_games_list validation for the score parameter."""
        # Valid score
        try:
            self.client.get_games_list(score={"gameplay": 5, "control": 10})
        except ValueError:
            self.fail("get_games_list raised ValueError unexpectedly for score!")

        # Invalid value (string)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(score={"gameplay": "invalid"})
        self.assertIn("Invalid score value for 'gameplay': invalid", str(cm.exception))

        # Invalid value (out of range)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(score={"gameplay": 11})
        self.assertIn("Invalid score value for 'gameplay': 11", str(cm.exception))
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(score={"control": -1})
        self.assertIn("Invalid score value for 'control': -1", str(cm.exception))

        # Invalid key
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(score={"invalid_key": 5})
        self.assertIn("Invalid score key: 'invalid_key'", str(cm.exception))

        # Invalid type (not a dict)
        with self.assertRaises(ValueError) as cm:
            self.client.get_games_list(score="invalid_score")
        self.assertIn("Score parameter must be a dictionary", str(cm.exception))

    def test_get_games_list_validation_success(self, mock_fetch):
        """Test get_games_list validation with valid parameters."""
        try:
            self.client.get_games_list(
                platforms=[Platform.ANDROID],
                players=["singleplayer"],
                category=["action"],
                tags=["2d", "pixel-art"],
                countries_android=["us"],
            )
        except ValueError:
            self.fail("get_games_list raised ValueError unexpectedly!")

    def test_get_games_list_validation_failure(self, mock_fetch):
        """Test get_games_list validation with invalid parameters."""
        with self.assertRaises(ValueError):
            self.client.get_games_list(category=["invalid-category"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(players=["invalid-player"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(network=["invalid-network"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(monetization_android=["invalid-monetization"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(monetization_ios=["invalid-monetization"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(screen_orientation=["invalid-orientation"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(sub_category=["invalid-sub-category"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(tags=["invalid-tag"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(countries_android=["invalid-country"])
        with self.assertRaises(ValueError):
            self.client.get_games_list(countries_ios=["invalid-country"])

    def test_get_similar_games_validation(self, mock_fetch):
        """Test get_similar_games validation."""
        with self.assertRaises(ValueError):
            self.client.get_similar_games(
                game_id=1, platforms=[Platform.ANDROID, "invalid-platform"]
            )
        try:
            self.client.get_similar_games(game_id=1, platforms=[Platform.IOS])
        except ValueError:
            self.fail("get_similar_games raised ValueError unexpectedly!")

    def test_get_home_validation(self, mock_fetch):
        """Test get_home validation."""
        with self.assertRaises(ValueError):
            self.client.get_home(platforms=["invalid-platform"])
        try:
            self.client.get_home(platforms=[Platform.ANDROID])
        except ValueError:
            self.fail("get_home raised ValueError unexpectedly!")

    def test_get_games_of_the_week_validation(self, mock_fetch):
        """Test get_games_of_the_week validation."""
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(platforms=["invalid-platform"])
        try:
            self.client.get_games_of_the_week(platforms=[Platform.IOS])
        except ValueError:
            self.fail("get_games_of_the_week raised ValueError unexpectedly!")

    def test_get_top_user_ratings_validation(self, mock_fetch):
        """Test get_top_user_ratings validation."""
        with self.assertRaises(ValueError):
            self.client.get_top_user_ratings(platforms=["invalid-platform"])
        try:
            self.client.get_top_user_ratings(platforms=[Platform.ANDROID, Platform.IOS])
        except ValueError:
            self.fail("get_top_user_ratings raised ValueError unexpectedly!")

    def test_get_upcoming_games_validation(self, mock_fetch):
        """Test get_upcoming_games validation."""
        with self.assertRaises(ValueError):
            self.client.get_upcoming_games(platforms=["invalid-platform"])
        try:
            self.client.get_upcoming_games(platforms=[Platform.ANDROID])
        except ValueError:
            self.fail("get_upcoming_games raised ValueError unexpectedly!")

    def test_get_categories_validation(self, mock_fetch):
        """Test get_categories validation."""
        with self.assertRaises(ValueError):
            self.client.get_categories(platforms=["invalid-platform"])
        try:
            self.client.get_categories(platforms=[Platform.ANDROID])
        except ValueError:
            self.fail("get_categories raised ValueError unexpectedly!")


class TestBuildParams(unittest.TestCase):
    """A test suite for the _build_params method."""

    def setUp(self):
        """Set up a new client for each test."""
        self.client = MiniReviewClient()

    def test_none_and_empty_values(self):
        """Test that None and empty values are ignored."""
        params = {
            "a": None,
            "b": "",
            "c": [],
            "d": {},
            "e": "value",
        }
        processed_params = self.client._build_params(params)
        self.assertEqual(processed_params, {"e": "value"})

    def test_enum_value(self):
        """Test that an Enum is converted to its value."""
        params = {"orderBy": OrderBy.MOST_POPULAR}
        processed_params = self.client._build_params(params)
        self.assertEqual(processed_params, {"orderBy": "most-popular"})

    def test_list_of_strings(self):
        """Test a list of strings."""
        params = {"tags": ["2d", "3d"]}
        processed_params = self.client._build_params(params)
        self.assertEqual(processed_params, {"tags": "2d,3d"})

    def test_list_of_enums(self):
        """Test a list of enums."""
        params = {"platforms": [Platform.ANDROID, Platform.IOS]}
        processed_params = self.client._build_params(params)
        self.assertEqual(
            processed_params, {"platforms[0]": "android", "platforms[1]": "ios"}
        )

    def test_score_dict(self):
        """Test the score dictionary."""
        params = {"score": {"min": 80, "max": 100}}
        processed_params = self.client._build_params(params)
        self.assertEqual(processed_params, {"score": "min-80,max-100"})

    def test_boolean_values(self):
        """Test boolean to integer conversion."""
        params = {"is_new": True, "is_updated": False}
        processed_params = self.client._build_params(params)
        self.assertEqual(processed_params, {"is_new": 1, "is_updated": 0})

    def test_mixed_types(self):
        """Test a mix of all supported types."""
        params = {
            "page": 1,
            "limit": 50,
            "search": "test",
            "orderBy": OrderBy.LAST_ADDED_REVIEWS,
            "platforms": [Platform.ANDROID],
            "tags": ["pixel-art"],
            "score": {"min": 90},
            "is_free": True,
            "not_present": None,
            "empty_list": [],
        }
        processed_params = self.client._build_params(params)
        expected = {
            "page": 1,
            "limit": 50,
            "search": "test",
            "orderBy": "last-added-reviews",
            "platforms[0]": "android",
            "tags": "pixel-art",
            "score": "min-90",
            "is_free": 1,
        }
        self.assertEqual(processed_params, expected)

    def test_empty_params(self):
        """Test that an empty params dict results in an empty dict."""
        processed_params = self.client._build_params({})
        self.assertEqual(processed_params, {})

    def test_url_encoding(self):
        """Test the URL encoding of a complex parameter dictionary."""
        from urllib.parse import unquote

        params = {
            "page": 1,
            "limit": 50,
            "search": "rpg",
            "orderBy": OrderBy.LAST_ADDED_REVIEWS,
            "platforms": [Platform.ANDROID, Platform.IOS],
            "players": ["singleplayer"],
            "network": ["offline"],
            "monetization_android": ["free", "paid"],
            "monetization_ios": ["free"],
            "screen_orientation": ["landscape"],
            "category": ["action", "adventure"],
            "sub_category": ["rpg"],
            "tags": ["2d", "3d"],
            "countries_android": ["us", "br"],
            "countries_ios": ["ca"],
            "score": {"min": 8, "max": 10},
            "loadNewcollections": True,
            "loadLastUpdatedcollections": False,
        }

        processed_params = self.client._build_params(params)
        req = requests.Request("GET", "https://example.com", params=processed_params)
        prepared_req = req.prepare()
        query_string = unquote(prepared_req.url.split("?")[1])
        actual_params = sorted(query_string.split("&"))

        expected_params = sorted(
            [
                "page=1",
                "limit=50",
                "search=rpg",
                "orderBy=last-added-reviews",
                "platforms[0]=android",
                "platforms[1]=ios",
                "players=singleplayer",
                "network=offline",
                "monetization_android=free,paid",
                "monetization_ios=free",
                "screen_orientation=landscape",
                "category=action,adventure",
                "sub_category=rpg",
                "tags=2d,3d",
                "countries_android=us,br",
                "countries_ios=ca",
                "score=min-8,max-10",
                "loadNewcollections=1",
                "loadLastUpdatedcollections=0",
            ]
        )

        self.assertEqual(actual_params, expected_params)


@patch("minireview_client.client.MiniReviewClient._fetch_api", return_value=True)
class TestFilterMethods(unittest.TestCase):
    """A test suite for the filter helper methods."""

    def setUp(self):
        """Set up a new client and mock get_filters for each test."""
        self.client = MiniReviewClient()
        self.mock_filters_response = [
            {
                "slug": "players",
                "itens": [
                    {"slug": "singleplayer", "nome": "Singleplayer"},
                    {"slug": "multiplayer", "nome": "Multiplayer"},
                ],
            },
            {
                "slug": "countries-android",
                "itens": [
                    {"slug": "us", "nome": "United States"},
                    {"slug": "br", "nome": "Brazil"},
                ],
            },
            {"slug": "network", "itens": [{"slug": "online", "nome": "Online"}]},
            {
                "slug": "monetization-android",
                "itens": [{"slug": "free", "nome": "Free"}],
            },
            {"slug": "monetization-ios", "itens": [{"slug": "paid", "nome": "Paid"}]},
            {
                "slug": "screen-orientation",
                "itens": [{"slug": "portrait", "nome": "Portrait"}],
            },
            {"slug": "category", "itens": [{"slug": "action", "nome": "Action"}]},
            {"slug": "sub-category", "itens": [{"slug": "rpg", "nome": "RPG"}]},
            {"slug": "score", "itens": [{"slug": "gameplay", "nome": "Gameplay"}]},
        ]
        self.client.get_filters = unittest.mock.Mock(
            return_value=self.mock_filters_response
        )

    def test_get_filter_options(self, mock_fetch_api):
        """Test that the filter helper methods return the correct data."""
        players = self.client.get_players()
        self.assertEqual(
            players, {"singleplayer": "Singleplayer", "multiplayer": "Multiplayer"}
        )

        countries = self.client.get_countries_android()
        self.assertEqual(countries, {"us": "United States", "br": "Brazil"})

        network = self.client.get_network_options()
        self.assertEqual(network, {"online": "Online"})

        monetization_android = self.client.get_monetization_android()
        self.assertEqual(monetization_android, {"free": "Free"})

        monetization_ios = self.client.get_monetization_ios()
        self.assertEqual(monetization_ios, {"paid": "Paid"})

        screen_orientation = self.client.get_screen_orientation_options()
        self.assertEqual(screen_orientation, {"portrait": "Portrait"})

        category = self.client.get_category_options()
        self.assertEqual(category, {"action": "Action"})

        sub_category = self.client.get_sub_category_options()
        self.assertEqual(sub_category, {"rpg": "RPG"})

        score = self.client.get_score_options()
        self.assertEqual(score, {"gameplay": "Gameplay"})

        # Test a filter that doesn't exist
        non_existent = self.client._get_filter_options("non-existent-filter")
        self.assertEqual(non_existent, {})


if __name__ == "__main__":
    unittest.main()
