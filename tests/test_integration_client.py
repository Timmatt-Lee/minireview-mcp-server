"""
Integration tests for the MiniReviewClient that make live API calls.
"""
import pytest
import vcr

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    CollectionsOrderBy,
    GamesListOrderBy,
    Monetization,
    Platform,
    Players,
    ScreenOrientation,
)


@pytest.fixture(scope="module")
@vcr.use_cassette("tests/cassettes/test_integration_client/setup.yaml")
def game_data():
    """Set up a new client and fetch initial data for all tests."""
    try:
        client = MiniReviewClient()
        # Use a common game to ensure data is available
        games_data = client.get_games_list(limit=1, search="Merge Dragons!")
        if games_data and games_data.get("data"):
            game = games_data["data"][0]
            return {
                "client": client,
                "game_id": game.get("id"),
                "game_slug": game.get("slug"),
                "game_category": game.get("categoria", {}).get("slug"),
            }
        pytest.fail("Failed to fetch initial game data: No data found.")
    except Exception as e:
        pytest.fail(f"Failed to fetch initial game data for tests: {e}")


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_games_list_comprehensive.yaml"
)
def test_get_games_list_comprehensive(game_data):
    """Test get_games_list with a comprehensive set of parameters."""
    client = game_data["client"]
    filters = client.get_filters()

    def get_valid_filter_value(filter_slug):
        for f in filters:
            if f["slug"] == filter_slug and f["itens"]:
                return f["itens"][0]["slug"]
        return None

    score_keys = []
    for f in filters:
        if f["slug"] == "score":
            score_keys = [item["slug"] for item in f["itens"]]
            break

    score_param = {key: 5 for key in score_keys}

    params = {
        "limit": 1,
        "search": "rpg",
        "orderBy": GamesListOrderBy.HIGHEST_SCORE,
        "platforms": [Platform.ANDROID],
        "players": [Players.SINGLE_PLAYER],
        "network": [get_valid_filter_value("network")]
        if get_valid_filter_value("network")
        else [],
        "monetization_android": [get_valid_filter_value("monetization-android")]
        if get_valid_filter_value("monetization-android")
        else [],
        "monetization_ios": [get_valid_filter_value("monetization-ios")]
        if get_valid_filter_value("monetization-ios")
        else [],
        "screen_orientation": [get_valid_filter_value("screen-orientation")]
        if get_valid_filter_value("screen-orientation")
        else [],
        "category": [get_valid_filter_value("category")]
        if get_valid_filter_value("category")
        else [],
        "sub_category": [get_valid_filter_value("sub-category")]
        if get_valid_filter_value("sub-category")
        else [],
        "tags": [get_valid_filter_value("tags")]
        if get_valid_filter_value("tags")
        else [],
        "countries_android": [get_valid_filter_value("countries-android")]
        if get_valid_filter_value("countries-android")
        else [],
        "countries_ios": [get_valid_filter_value("countries-ios")]
        if get_valid_filter_value("countries-ios")
        else [],
        "score": score_param,
    }
    response = client.get_games_list(**params)
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_countries_android.yaml"
)
def test_get_countries_android(game_data):
    """Test a live call to get_countries_android."""
    response = game_data["client"].get_countries_android()
    assert isinstance(response, dict)
    assert "us" in response  # Check for a common country code


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_game_details.yaml")
def test_get_game_details(game_data):
    """Test a live call to get_game_details."""
    game_slug = game_data["game_slug"]
    game_category = game_data["game_category"]

    if not game_slug or not game_category:
        pytest.skip("Skipping test: missing game slug or category from initial data.")

    response = game_data["client"].get_game_details(game_slug, game_category)
    assert "data" in response
    assert "nome" in response["data"]
    assert response["data"]["slug"] == game_slug


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_game_ratings.yaml")
def test_get_game_ratings(game_data):
    """Test a live call to get_game_ratings."""
    game_id = game_data["game_id"]
    if not game_id:
        pytest.skip("Skipping test: missing game ID from initial data.")

    response = game_data["client"].get_game_ratings(game_id)
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_similar_games_comprehensive.yaml"
)
def test_get_similar_games_comprehensive(game_data):
    """Test get_similar_games with a comprehensive set of parameters."""
    client = game_data["client"]
    game_id = game_data["game_id"]
    if not game_id:
        pytest.skip("Skipping test: missing game ID from initial data.")

    params = {
        "game_id": game_id,
        "limit": 1,
        "platforms": [Platform.ANDROID],
        "monetization": Monetization.FREE,
        "players": Players.SINGLE_PLAYER,
        "screen_orientation": ScreenOrientation.LANDSCAPE,
    }
    response = client.get_similar_games(**params)
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_collections.yaml")
def test_get_collections(game_data):
    """Test a live call to get_collections."""
    response = game_data["client"].get_collections(
        limit=1, is_load_new=True, is_load_last_updated=True
    )
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_collections_comprehensive.yaml"
)
def test_get_collections_comprehensive(game_data):
    """Test get_collections with a comprehensive set of parameters."""
    client = game_data["client"]

    params = {
        "limit": 1,
        "search": "rpg",
        "orderBy": CollectionsOrderBy.NEWEST,
        "is_load_new": True,
        "is_load_last_updated": False,
    }
    response = client.get_collections(**params)
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_home.yaml")
def test_get_home(game_data):
    """Test a live call to get_home."""
    response = game_data["client"].get_home(platforms=[Platform.ANDROID])
    assert "data" in response


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_games_of_the_week.yaml"
)
def test_get_games_of_the_week(game_data):
    """Test a live call to get_games_of_the_week."""
    response = game_data["client"].get_games_of_the_week(platforms=[Platform.ANDROID])
    assert "data" in response


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_top_user_ratings.yaml"
)
def test_get_top_user_ratings(game_data):
    """Test a live call to get_top_user_ratings."""
    response = game_data["client"].get_top_user_ratings(platforms=[Platform.ANDROID])
    assert "data" in response


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_upcoming_games.yaml")
def test_get_upcoming_games(game_data):
    """Test a live call to get_upcoming_games."""
    response = game_data["client"].get_upcoming_games(platforms=[Platform.ANDROID])
    assert "data" in response


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_top_games.yaml")
def test_get_top_games(game_data):
    """Test a live call to get_top_games."""
    response = game_data["client"].get_top_games()
    assert "data" in response


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_categories.yaml")
def test_get_categories(game_data):
    """Test a live call to get_categories."""
    response = game_data["client"].get_categories()
    assert "data" in response
    assert isinstance(response["data"], list)
