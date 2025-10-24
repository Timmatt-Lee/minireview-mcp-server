import json

import pytest
from fastmcp import Client, FastMCP

from server import (
    get_category_options,
    get_countries_android_options,
    get_countries_ios_options,
    get_game_details,
    get_game_ratings,
    get_games_list,
    get_games_of_the_week,
    get_home,
    get_minireview_pick,
    get_monetization_android_options,
    get_monetization_ios_options,
    get_network_options,
    get_player_options,
    get_score_options,
    get_screen_orientation_options,
    get_similar_games,
    get_sub_category_options,
    get_tag_options,
    get_top_user_ratings,
    get_upcoming_games,
)


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_games_list_integration():
    app = FastMCP()
    app.tool(get_games_list.fn)

    async with Client(app) as client:
        result = await client.call_tool("get_games_list", {"limit": 1})
        data = json.loads(result.content[0].text)

        assert isinstance(data, dict)
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        game = data["data"][0]
        assert game.get("id") is not None
        assert game.get("name") is not None
        assert game.get("slug") is not None
        assert game.get("total_reviews") is not None
        assert game.get("positive_review_percentage") is not None
        assert game.get("platform") is not None
        assert game["platform"].get("android") is not None
        assert game["platform"]["android"].get("is_available") is not None
        assert game["platform"].get("ios") is not None
        assert game["platform"]["ios"].get("is_available") is not None
        assert game.get("category") is not None
        assert game.get("categories") is not None
        assert game.get("description") is not None
        assert game.get("price") is not None


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_game_details_integration():
    app = FastMCP()
    app.tool(get_games_list.fn)
    app.tool(get_game_details.fn)

    async with Client(app) as client:
        # First, get a list of games to find a valid game to test with
        list_result = await client.call_tool("get_games_list", {"limit": 1})
        list_data = json.loads(list_result.content[0].text)
        game = list_data["data"][0]
        game_slug = game["slug"]
        category_slug = game["category"]["slug"]

        # Now, call get_game_details with the real data
        details_result = await client.call_tool(
            "get_game_details", {"game_slug": game_slug, "category": category_slug}
        )
        details_data = json.loads(details_result.content[0].text)

        # Assert the structure of the trimmed and translated response
        assert isinstance(details_data, dict)
        assert details_data.get("id") is not None
        assert details_data.get("name") is not None
        assert details_data.get("slug") is not None
        assert details_data.get("score") is not None
        assert details_data.get("total_reviews") is not None
        assert details_data.get("platform") is not None
        assert details_data["platform"].get("android") is not None
        assert details_data["platform"]["android"].get("is_available") is not None
        assert details_data["platform"]["android"].get("is_dead") is not None
        assert details_data["platform"].get("ios") is not None
        assert details_data["platform"]["ios"].get("is_available") is not None
        assert details_data["platform"]["ios"].get("is_dead") is not None
        assert details_data.get("category") is not None
        assert details_data.get("subcategory") is not None
        assert details_data.get("categories") is not None
        assert details_data.get("top_game") is not None
        assert details_data.get("is_minireview_pick") is not None
        assert details_data.get("is_game_of_week") is not None
        assert details_data.get("description") is not None
        assert details_data.get("review") is not None
        assert details_data.get("spec") is not None
        assert details_data.get("tags") is not None


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_game_ratings_integration():
    app = FastMCP()
    app.tool(get_games_list.fn)
    app.tool(get_game_ratings.fn)

    async with Client(app) as client:
        list_result = await client.call_tool("get_games_list", {"limit": 1})
        list_data = json.loads(list_result.content[0].text)
        game_id = list_data["data"][0]["id"]

        ratings_result = await client.call_tool(
            "get_game_ratings", {"game_id": game_id, "limit": 1}
        )
        ratings_data = json.loads(ratings_result.content[0].text)

        assert isinstance(ratings_data, dict)
        assert "data" in ratings_data
        assert isinstance(ratings_data["data"], list)
        assert "current_page" in ratings_data
        assert "total_ratings" in ratings_data
        assert "total_positive_ratings" in ratings_data
        assert "total_negative_ratings" in ratings_data
        assert "is_last_page" in ratings_data
        assert "positive_percentage" in ratings_data

        if ratings_data["data"]:
            rating = ratings_data["data"][0]
            assert "id" in rating
            assert "date" in rating
            assert "score" in rating
            assert "text" in rating
            assert "type" in rating


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_similar_games_integration():
    app = FastMCP()
    app.tool(get_games_list.fn)
    app.tool(get_similar_games.fn)

    async with Client(app) as client:
        list_result = await client.call_tool("get_games_list", {"limit": 1})
        list_data = json.loads(list_result.content[0].text)
        game_id = list_data["data"][0]["id"]

        similar_games_result = await client.call_tool(
            "get_similar_games", {"game_id": game_id, "limit": 1}
        )
        similar_games_data = json.loads(similar_games_result.content[0].text)

        assert isinstance(similar_games_data, dict)
        assert "data" in similar_games_data
        assert isinstance(similar_games_data["data"], list)
        assert len(similar_games_data["data"]) > 0

        game = similar_games_data["data"][0]
        assert game.get("id") is not None
        assert game.get("name") is not None
        assert game.get("slug") is not None
        assert game.get("total_likes") is not None
        assert game.get("total_dislikes") is not None
        assert game.get("platform") is not None
        assert game["platform"].get("android") is not None
        assert game["platform"]["android"].get("is_available") is not None
        assert game["platform"].get("ios") is not None
        assert game["platform"]["ios"].get("is_available") is not None
        assert game.get("category") is not None
        assert game.get("categories") is not None
        assert game.get("description") is not None
        assert game.get("price") is not None

        assert "total_games" in similar_games_data
        assert "is_last_page" in similar_games_data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_home_integration():
    app = FastMCP()
    app.tool(get_home.fn)

    async with Client(app) as client:
        result = await client.call_tool("get_home")
        data = json.loads(result.content[0].text)

        assert isinstance(data, dict)


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_games_of_the_week_integration():
    app = FastMCP()
    app.tool(get_games_of_the_week.fn)

    async with Client(app) as client:
        result = await client.call_tool("get_games_of_the_week", {"limit": 1})
        data = json.loads(result.content[0].text)

        assert isinstance(data, dict)
        assert "data" in data
        assert isinstance(data["data"], list)


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_minireview_pick_integration():
    app = FastMCP()
    app.tool(get_minireview_pick.fn)

    async with Client(app) as client:
        result = await client.call_tool("get_minireview_pick", {"limit": 1})
        data = json.loads(result.content[0].text)

        assert isinstance(data, dict)
        assert "data" in data
        assert isinstance(data["data"], list)


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_top_user_ratings_integration():
    app = FastMCP()
    app.tool(get_top_user_ratings.fn)

    async with Client(app) as client:
        result = await client.call_tool("get_top_user_ratings", {"limit": 1})
        data = json.loads(result.content[0].text)

        assert isinstance(data, dict)


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_upcoming_games_integration():
    app = FastMCP()
    app.tool(get_upcoming_games.fn)

    async with Client(app) as client:
        result = await client.call_tool("get_upcoming_games", {"limit": 1})
        data = json.loads(result.content[0].text)

        assert isinstance(data, dict)
        assert "data" in data
        assert isinstance(data["data"], list)


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_player_options_integration():
    app = FastMCP()
    app.tool(get_player_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_player_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_network_options_integration():
    app = FastMCP()
    app.tool(get_network_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_network_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_monetization_android_options_integration():
    app = FastMCP()
    app.tool(get_monetization_android_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_monetization_android_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_monetization_ios_options_integration():
    app = FastMCP()
    app.tool(get_monetization_ios_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_monetization_ios_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_screen_orientation_options_integration():
    app = FastMCP()
    app.tool(get_screen_orientation_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_screen_orientation_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_category_options_integration():
    app = FastMCP()
    app.tool(get_category_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_category_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_sub_category_options_integration():
    app = FastMCP()
    app.tool(get_sub_category_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_sub_category_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_tag_options_integration():
    app = FastMCP()
    app.tool(get_tag_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_tag_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_countries_android_options_integration():
    app = FastMCP()
    app.tool(get_countries_android_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_countries_android_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_countries_ios_options_integration():
    app = FastMCP()
    app.tool(get_countries_ios_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_countries_ios_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_get_score_options_integration():
    app = FastMCP()
    app.tool(get_score_options.fn)
    async with Client(app) as client:
        result = await client.call_tool("get_score_options")
        data = json.loads(result.content[0].text)
        assert isinstance(data, dict)
        assert "options" in data
