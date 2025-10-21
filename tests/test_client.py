"""
Unit tests for the MiniReviewClient.
"""

import unittest
from unittest.mock import patch

import requests

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    GameRatingsOrderBy,
    GameRatingType,
    GamesListOrderBy,
    Monetization,
    Platform,
    Players,
    ScreenOrientation,
    TopUserRatingsOrderBy,
)
from minireview_client.exceptions import APIError


class TestCoreClientFeatures(unittest.TestCase):
    """Test suite for core client features like init, caching, and errors."""

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
@patch("minireview_client.client.MiniReviewClient._init_validator", return_value=None)
class TestApiClientCalls(unittest.TestCase):
    """A test suite for happy-path API method calls."""

    def setUp(self):
        """Set up a new client for each test."""
        self.client = MiniReviewClient()
        # Mock the parsed filters to prevent assertion errors in the validator,
        # which is called by some of the client methods before fetching the API.
        self.client._parsed_filters = {"score": {"gameplay"}}

    def test_get_game_details_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_game_details calls _fetch_api with correct params."""
        game_slug = "my-game"
        category = "action"

        self.client.get_game_details(game_slug, category)

        # get_game_details does not validate, so _init_validator should not be called.
        mock_init_validator.assert_not_called()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], f"/games/{game_slug}")
        self.assertEqual(call_args[1]["getBy"], "slug")
        self.assertEqual(call_args[1]["category"], category)

    def test_get_game_ratings_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_game_ratings calls _fetch_api with correct params."""
        self.client.get_game_ratings(
            game_id=123,
            orderBy=GameRatingsOrderBy.MOST_RELEVANT,
            type=GameRatingType.ALL,
        )

        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/games-ratings")
        self.assertEqual(call_args[1]["orderBy"], "most-relevant")
        self.assertEqual(call_args[1]["type"], "all")
        self.assertEqual(call_args[1]["game_id"], 123)

    def test_get_games_list_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_games_list calls _fetch_api with correct params."""
        self.client.get_games_list(search="rpg", orderBy=GamesListOrderBy.HIGHEST_SCORE)
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/games")
        self.assertEqual(call_args[1]["search"], "rpg")
        self.assertEqual(call_args[1]["orderBy"], "highest-score")

    def test_get_similar_games_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_similar_games calls _fetch_api with correct params."""
        self.client.get_similar_games(game_id=123, players=Players.MULTI_PLAYER)
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/games-similar")
        self.assertEqual(call_args[1]["game_id"], 123)
        self.assertEqual(call_args[1]["players"], "multiplayer")

    def test_get_home_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_home calls _fetch_api with correct params."""
        self.client.get_home(orderBy=GamesListOrderBy.NEW_ON_MINIREVIEW)
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/home")
        self.assertEqual(call_args[1]["orderBy"], "new-on-minireview")

    def test_get_games_of_the_week_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_games_of_the_week calls _fetch_api with correct params."""
        self.client.get_games_of_the_week(category=["action"])
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/games")
        self.assertEqual(call_args[1]["type"], "games-of-the-week")
        self.assertEqual(call_args[1]["category"], "action")

    def test_get_minireview_pick_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_minireview_pick calls _fetch_api with correct params."""
        self.client.get_minireview_pick(category=["rpg"])
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/games")
        self.assertEqual(call_args[1]["type"], "our-pick")
        self.assertEqual(call_args[1]["category"], "rpg")

    def test_get_top_user_ratings_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_top_user_ratings calls _fetch_api with correct params."""
        self.client.get_top_user_ratings(orderBy=TopUserRatingsOrderBy.ALL_TIME)
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/top-user-ratings")
        self.assertEqual(call_args[1]["orderBy"], "all-time")

    def test_get_upcoming_games_call(self, mock_init_validator, mock_fetch_api):
        """Test that get_upcoming_games calls _fetch_api with correct params."""
        self.client.get_upcoming_games(orderBy=GamesListOrderBy.RELEASE_DATE)
        mock_init_validator.assert_called_once()
        mock_fetch_api.assert_called_once()
        call_args = mock_fetch_api.call_args[0]
        self.assertEqual(call_args[0], "/upcoming-games")
        self.assertEqual(call_args[1]["orderBy"], "release-date")


@patch("minireview_client.client.MiniReviewClient._fetch_api", return_value=True)
@patch("minireview_client.client.MiniReviewClient._init_validator", return_value=None)
class TestParameterValidation(unittest.TestCase):
    """A test suite for all parameter validation in the client."""

    def setUp(self):
        """Set up a new client for each test."""
        self.client = MiniReviewClient()
        mock_filters = {
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
        self.client._parsed_filters = mock_filters

    def test_get_games_list_score_validation(self, mock_init, mock_fetch):
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

    def test_get_games_list_validation_success(self, mock_init, mock_fetch):
        """Test get_games_list validation with valid parameters."""
        try:
            self.client.get_games_list(
                orderBy=GamesListOrderBy.HIGHEST_SCORE,
                platforms=[Platform.ANDROID],
                players=["singleplayer"],
                category=["action"],
                tags=["2d", "pixel-art"],
                countries_android=["us"],
            )
        except (ValueError, TypeError):
            self.fail("get_games_list raised an exception unexpectedly!")

    def test_get_games_list_validation_failure(self, mock_init, mock_fetch):
        """Test get_games_list validation with invalid parameters."""
        with self.assertRaises(TypeError):
            self.client.get_games_list(orderBy="invalid-orderby")
        with self.assertRaises(TypeError):
            self.client.get_games_list(platforms=["invalid-platform"])
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

    def test_get_game_ratings_validation(self, mock_init, mock_fetch):
        """Test get_game_ratings validation."""
        with self.assertRaises(TypeError):
            self.client.get_game_ratings(game_id=1, type="invalid-type")
        with self.assertRaises(TypeError):
            self.client.get_game_ratings(game_id=1, orderBy="invalid-orderby")
        try:
            self.client.get_game_ratings(
                game_id=1, type=GameRatingType.ALL, orderBy=GameRatingsOrderBy.NEWEST
            )
        except (ValueError, TypeError):
            self.fail("get_game_ratings raised an exception unexpectedly!")

    def test_get_similar_games_validation(self, mock_init, mock_fetch):
        """Test get_similar_games validation."""
        with self.assertRaises(TypeError):
            self.client.get_similar_games(game_id=1, platforms=["invalid-platform"])
        with self.assertRaises(TypeError):
            self.client.get_similar_games(
                game_id=1, monetization="invalid-monetization"
            )
        with self.assertRaises(TypeError):
            self.client.get_similar_games(game_id=1, players="invalid-player")
        with self.assertRaises(TypeError):
            self.client.get_similar_games(
                game_id=1, screen_orientation="invalid-orientation"
            )
        try:
            self.client.get_similar_games(
                game_id=1,
                platforms=[Platform.IOS],
                monetization=Monetization.FREE,
                players=Players.SINGLE_PLAYER,
                screen_orientation=ScreenOrientation.PORTRAIT,
            )
        except (ValueError, TypeError):
            self.fail("get_similar_games raised an exception unexpectedly!")

    def test_get_home_validation(self, mock_init, mock_fetch):
        """Test get_home validation."""
        with self.assertRaises(TypeError):
            self.client.get_home(platforms=["invalid-platform"])
        with self.assertRaises(TypeError):
            self.client.get_home(orderBy="invalid-orderby")
        try:
            self.client.get_home(
                platforms=[Platform.ANDROID],
                orderBy=GamesListOrderBy.LAST_ADDED_REVIEWS,
            )
        except (ValueError, TypeError):
            self.fail("get_home raised an exception unexpectedly!")

    def test_get_games_of_the_week_validation(self, mock_init, mock_fetch):
        """Test get_games_of_the_week validation."""
        with self.assertRaises(TypeError):
            self.client.get_games_of_the_week(platforms=["invalid-platform"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(category=["invalid-category"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(players=["invalid-player"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(network=["invalid-network"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(
                monetization_android=["invalid-monetization"]
            )
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(monetization_ios=["invalid-monetization"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(
                screen_orientation=["invalid-orientation"]
            )
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(sub_category=["invalid-sub-category"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(tags=["invalid-tag"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(countries_android=["invalid-country"])
        with self.assertRaises(ValueError):
            self.client.get_games_of_the_week(countries_ios=["invalid-country"])
        try:
            self.client.get_games_of_the_week(platforms=[Platform.IOS])
        except (ValueError, TypeError):
            self.fail("get_games_of_the_week raised an exception unexpectedly!")

    def test_get_minireview_pick_validation(self, mock_init, mock_fetch):
        """Test get_minireview_pick validation."""
        with self.assertRaises(TypeError):
            self.client.get_minireview_pick(platforms=["invalid-platform"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(category=["invalid-category"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(players=["invalid-player"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(network=["invalid-network"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(
                monetization_android=["invalid-monetization"]
            )
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(monetization_ios=["invalid-monetization"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(screen_orientation=["invalid-orientation"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(sub_category=["invalid-sub-category"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(tags=["invalid-tag"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(countries_android=["invalid-country"])
        with self.assertRaises(ValueError):
            self.client.get_minireview_pick(countries_ios=["invalid-country"])
        try:
            self.client.get_minireview_pick(platforms=[Platform.IOS])
        except (ValueError, TypeError):
            self.fail("get_minireview_pick raised an exception unexpectedly!")

    def test_get_top_user_ratings_validation(self, mock_init, mock_fetch):
        """Test get_top_user_ratings validation."""
        with self.assertRaises(TypeError):
            self.client.get_top_user_ratings(platforms=["invalid-platform"])
        with self.assertRaises(TypeError):
            self.client.get_top_user_ratings(orderBy="invalid-orderby")
        try:
            self.client.get_top_user_ratings(
                platforms=[Platform.ANDROID, Platform.IOS],
                orderBy=TopUserRatingsOrderBy.THIS_WEEK,
            )
        except (ValueError, TypeError):
            self.fail("get_top_user_ratings raised an exception unexpectedly!")

    def test_get_upcoming_games_validation(self, mock_init, mock_fetch):
        """Test get_upcoming_games validation."""
        with self.assertRaises(TypeError):
            self.client.get_upcoming_games(platforms=["invalid-platform"])
        with self.assertRaises(TypeError):
            self.client.get_upcoming_games(orderBy="invalid-orderby")
        try:
            self.client.get_upcoming_games(
                platforms=[Platform.ANDROID], orderBy=GamesListOrderBy.RELEASE_DATE
            )
        except (ValueError, TypeError):
            self.fail("get_upcoming_games raised an exception unexpectedly!")

    def test_get_game_details_validation(self, mock_init, mock_fetch):
        """Test get_game_details validation."""
        with self.assertRaises(ValueError) as cm:
            self.client.get_game_details(game_slug="", category="action")
        self.assertIn("game_slug cannot be empty", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            self.client.get_game_details(game_slug="my-game", category="")
        self.assertIn("category cannot be empty", str(cm.exception))

        try:
            self.client.get_game_details(game_slug="my-game", category="action")
        except ValueError:
            self.fail("get_game_details raised ValueError unexpectedly!")


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
            "orderBy": GamesListOrderBy.LAST_ADDED_REVIEWS,
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
            "orderBy": GamesListOrderBy.LAST_ADDED_REVIEWS,
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
