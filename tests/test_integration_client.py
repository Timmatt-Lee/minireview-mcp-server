"""
Integration tests for the MiniReviewClient that make live API calls.
"""
import pytest
import vcr

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


@pytest.fixture(scope="module")
def filters_data(game_data):
    """Get the filters from the client."""
    return game_data["client"].get_filters()


def _build_params(filters, filter_slugs):
    """Build a dictionary of parameters for the API calls."""

    def get_valid_filter_value(filter_slug):
        for f in filters:
            if f["slug"] == filter_slug and f["itens"]:
                return f["itens"][0]["slug"]
        return None

    params = {}
    for slug in filter_slugs:
        value = get_valid_filter_value(slug)
        if value:
            params[slug.replace("-", "_")] = [value]

    score_keys = []
    for f in filters:
        if f["slug"] == "score":
            score_keys = [item["slug"] for item in f["itens"]]
            break
    if score_keys:
        params["score"] = {key: 5 for key in score_keys}

    return params


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_games_list.yaml")
def test_get_games_list(game_data, filters_data):
    """Test get_games_list with a comprehensive set of parameters."""
    client = game_data["client"]
    filter_slugs = [
        "network",
        "monetization-android",
        "monetization-ios",
        "screen-orientation",
        "category",
        "sub-category",
        "tags",
        "countries-android",
        "countries-ios",
    ]
    params = _build_params(filters_data, filter_slugs)
    params.update(
        {
            "limit": 1,
            "search": "rpg",
            "orderBy": GamesListOrderBy.HIGHEST_SCORE,
            "platforms": [Platform.ANDROID],
            "players": [Players.SINGLE_PLAYER],
        }
    )
    response = client.get_games_list(**params)
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_players(game_data):
    """Test a live call to get_players."""
    response = game_data["client"].get_players()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_network_options(game_data):
    """Test a live call to get_network_options."""
    response = game_data["client"].get_network_options()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_monetization_android(game_data):
    """Test a live call to get_monetization_android."""
    response = game_data["client"].get_monetization_android()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_monetization_ios(game_data):
    """Test a live call to get_monetization_ios."""
    response = game_data["client"].get_monetization_ios()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_screen_orientation_options(game_data):
    """Test a live call to get_screen_orientation_options."""
    response = game_data["client"].get_screen_orientation_options()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_category_options(game_data):
    """Test a live call to get_category_options."""
    response = game_data["client"].get_category_options()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_sub_category_options(game_data):
    """Test a live call to get_sub_category_options."""
    response = game_data["client"].get_sub_category_options()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_tags(game_data):
    """Test a live call to get_tags."""
    response = game_data["client"].get_tags()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_countries_android(game_data):
    """Test a live call to get_countries_android."""
    response = game_data["client"].get_countries_android()
    assert isinstance(response, dict)
    assert "us" in response  # Check for a common country code


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_countries_ios(game_data):
    """Test a live call to get_countries_ios."""
    response = game_data["client"].get_countries_ios()
    assert isinstance(response, dict)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_filters.yaml")
def test_get_score_options(game_data):
    """Test a live call to get_score_options."""
    response = game_data["client"].get_score_options()
    assert isinstance(response, dict)


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
    """Test get_game_ratings with a comprehensive set of parameters."""
    client = game_data["client"]
    game_id = game_data["game_id"]
    if not game_id:
        pytest.skip("Skipping test: missing game ID from initial data.")

    params = {
        "game_id": game_id,
        "page": 2,
        "limit": 10,
        "type": GameRatingType.POSITIVE,
        "orderBy": GameRatingsOrderBy.OLDEST,
    }
    response = client.get_game_ratings(**params)
    assert "data" in response
    assert isinstance(response["data"], list)


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_similar_games.yaml")
def test_get_similar_games(game_data):
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


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_home.yaml")
def test_get_home(game_data):
    """Test get_home with a comprehensive set of parameters."""
    client = game_data["client"]
    params = {
        "page": 2,
        "platforms": [Platform.ANDROID],
        "ids_ignore": [1, 2, 3],
        "orderBy": GamesListOrderBy.NEW_ON_MINIREVIEW,
    }
    response = client.get_home(**params)
    assert "data" in response


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_games_of_the_week.yaml"
)
def test_get_games_of_the_week(game_data, filters_data):
    """Test get_games_of_the_week with a comprehensive set of parameters."""
    client = game_data["client"]
    filter_slugs = [
        "network",
        "monetization-android",
        "monetization-ios",
        "screen-orientation",
        "category",
        "sub-category",
        "tags",
        "countries-android",
        "countries-ios",
    ]
    params = _build_params(filters_data, filter_slugs)
    params.update(
        {
            "limit": 1,
            "platforms": [Platform.ANDROID],
            "players": [Players.SINGLE_PLAYER],
        }
    )
    response = client.get_games_of_the_week(**params)
    assert "data" in response


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_minireview_pick.yaml"
)
def test_get_minireview_pick(game_data, filters_data):
    """Test get_minireview_pick with a comprehensive set of parameters."""
    client = game_data["client"]
    filter_slugs = [
        "network",
        "monetization-android",
        "monetization-ios",
        "screen-orientation",
        "category",
        "sub-category",
        "tags",
        "countries-android",
        "countries-ios",
    ]
    params = _build_params(filters_data, filter_slugs)
    params.update(
        {
            "limit": 1,
            "platforms": [Platform.ANDROID],
            "players": [Players.SINGLE_PLAYER],
        }
    )
    response = client.get_minireview_pick(**params)
    assert "data" in response


@pytest.mark.vcr(
    "tests/cassettes/test_integration_client/test_get_top_user_ratings.yaml"
)
def test_get_top_user_ratings(game_data):
    """Test get_top_user_ratings with a comprehensive set of parameters."""
    client = game_data["client"]
    params = {
        "page": 2,
        "limit": 10,
        "orderBy": TopUserRatingsOrderBy.ALL_TIME,
        "platforms": [Platform.ANDROID],
    }
    response = client.get_top_user_ratings(**params)
    assert "data" in response


@pytest.mark.vcr("tests/cassettes/test_integration_client/test_get_upcoming_games.yaml")
def test_get_upcoming_games(game_data):
    """Test get_upcoming_games with a comprehensive set of parameters."""
    client = game_data["client"]
    params = {
        "page": 2,
        "limit": 10,
        "orderBy": GamesListOrderBy.RELEASE_DATE,
        "platforms": [Platform.ANDROID],
    }
    response = client.get_upcoming_games(**params)
    assert "data" in response
