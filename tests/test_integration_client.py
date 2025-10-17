"""
Integration tests for the MiniReviewClient that make live API calls.
"""

import unittest

import vcr

from minireview_client.client import MiniReviewClient
from minireview_client.enums import Platform


class TestIntegrationMiniReviewClient(unittest.TestCase):
    """A suite of integration tests for the MiniReviewClient."""

    @classmethod
    @vcr.use_cassette("tests/cassettes/test_integration_client/setup.yaml")
    def setUpClass(cls):
        """Set up a new client and fetch initial data for all tests."""
        cls.client = MiniReviewClient()
        cls.test_game_id = None
        cls.test_game_slug = None
        cls.test_game_category = None

        try:
            # Use a common game to ensure data is available
            games_data = cls.client.get_games_list(limit=1, search="Merge Dragons!")
            if games_data and games_data.get("data"):
                game = games_data["data"][0]
                cls.test_game_id = game.get("id")
                cls.test_game_slug = game.get("slug")
                if game.get("categoria"):
                    cls.test_game_category = game["categoria"].get("slug")
        except Exception as e:
            raise ConnectionError(f"Failed to fetch initial game data for tests: {e}")

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_games_list.yaml"
    )
    def test_get_games_list(self):
        """Test a live call to get_games_list."""
        response = self.client.get_games_list(limit=5)
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)
        self.assertGreater(len(response["data"]), 0)

    @vcr.use_cassette("tests/cassettes/test_integration_client/test_get_countries.yaml")
    def test_get_countries(self):
        """Test a live call to get_countries."""
        response = self.client.get_countries()
        self.assertIsInstance(response, dict)
        self.assertIn("us", response)  # Check for a common country code

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_game_details.yaml"
    )
    def test_get_game_details(self):
        """Test a live call to get_game_details."""
        if not self.test_game_slug or not self.test_game_category:
            self.skipTest(
                "Skipping test: missing game slug or category from initial data."
            )
        response = self.client.get_game_details(
            self.test_game_slug, self.test_game_category
        )
        self.assertIn("data", response)
        self.assertIn("nome", response["data"])
        self.assertEqual(response["data"]["slug"], self.test_game_slug)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_game_ratings.yaml"
    )
    def test_get_game_ratings(self):
        """Test a live call to get_game_ratings."""
        if not self.test_game_id:
            self.skipTest("Skipping test: missing game ID from initial data.")
        response = self.client.get_game_ratings(self.test_game_id)
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_similar_games.yaml"
    )
    def test_get_similar_games(self):
        """Test a live call to get_similar_games."""
        if not self.test_game_id:
            self.skipTest("Skipping test: missing game ID from initial data.")
        response = self.client.get_similar_games(self.test_game_id)
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_side_content.yaml"
    )
    def test_get_side_content(self):
        """Test a live call to get_side_content."""
        self.client.get_side_content(
            platforms=[Platform.ANDROID],
            content=["reviews", "topgames"],
        )

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_collections.yaml"
    )
    def test_get_collections(self):
        """Test a live call to get_collections."""
        response = self.client.get_collections(
            limit=1, is_load_new=True, is_load_last_updated=True
        )
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)

    @vcr.use_cassette("tests/cassettes/test_integration_client/test_get_home.yaml")
    def test_get_home(self):
        """Test a live call to get_home."""
        response = self.client.get_home(platforms=[Platform.ANDROID])
        self.assertIn("data", response)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_games_of_the_week.yaml"
    )
    def test_get_games_of_the_week(self):
        """Test a live call to get_games_of_the_week."""
        response = self.client.get_games_of_the_week(platforms=[Platform.ANDROID])
        self.assertIn("data", response)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_top_user_ratings.yaml"
    )
    def test_get_top_user_ratings(self):
        """Test a live call to get_top_user_ratings."""
        response = self.client.get_top_user_ratings(platforms=[Platform.ANDROID])
        self.assertIn("data", response)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_upcoming_games.yaml"
    )
    def test_get_upcoming_games(self):
        """Test a live call to get_upcoming_games."""
        response = self.client.get_upcoming_games(platforms=[Platform.ANDROID])
        self.assertIn("data", response)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_similar_games_main_page.yaml"
    )
    def test_get_similar_games_main_page(self):
        """Test a live call to get_similar_games_main_page."""
        response = self.client.get_similar_games_main_page(platforms=[Platform.ANDROID])
        self.assertIsNotNone(response)

    @vcr.use_cassette("tests/cassettes/test_integration_client/test_get_top_games.yaml")
    def test_get_top_games(self):
        """Test a live call to get_top_games."""
        response = self.client.get_top_games()
        self.assertIn("data", response)

    @vcr.use_cassette(
        "tests/cassettes/test_integration_client/test_get_categories.yaml"
    )
    def test_get_categories(self):
        """Test a live call to get_categories."""
        response = self.client.get_categories()
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)


if __name__ == "__main__":
    unittest.main()
