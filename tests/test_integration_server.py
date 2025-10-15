import json

import pytest
from fastmcp import Client, FastMCP

from server import (
    get_categories,
    get_collections,
    get_game_details,
    get_game_ratings,
    get_games_list,
    get_games_list_with_details,
    get_similar_games,
    get_similar_games_with_details,
)


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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
        category_slug = game["categoria"]["slug"]

        # Now, call get_game_details with the real data
        details_result = await client.call_tool(
            "get_game_details", {"game_slug": game_slug, "category": category_slug}
        )
        details_data = json.loads(details_result.content[0].text)

        # Assert the structure of the trimmed and translated response
        assert isinstance(details_data, dict)
        assert "id" in details_data
        assert "name" in details_data
        assert "slug" not in details_data
        assert "score" in details_data
        assert "category" in details_data
        assert "subcategory" in details_data
        assert "available_platforms" in details_data
        assert "android" in details_data["available_platforms"]
        assert "ios" in details_data["available_platforms"]


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_get_collections_integration():
    app = FastMCP()
    app.tool(get_collections.fn)

    async with Client(app) as client:
        collections_result = await client.call_tool("get_collections", {"limit": 1})
        collections_data = json.loads(collections_result.content[0].text)

        assert isinstance(collections_data, dict)
        assert "data" in collections_data
        assert isinstance(collections_data["data"], list)


@pytest.mark.asyncio
async def test_get_categories_integration():
    app = FastMCP()
    app.tool(get_categories.fn)

    async with Client(app) as client:
        categories_result = await client.call_tool("get_categories", {})
        categories_data = json.loads(categories_result.content[0].text)

        assert isinstance(categories_data, dict)
        assert "data" in categories_data
        assert isinstance(categories_data["data"], list)


@pytest.mark.asyncio
async def test_get_games_list_with_details_integration():
    app = FastMCP()
    app.tool(get_games_list_with_details.fn)

    async with Client(app) as client:
        games_with_details_result = await client.call_tool(
            "get_games_list_with_details", {"limit": 1}
        )
        games_with_details_data = json.loads(games_with_details_result.content[0].text)

        assert isinstance(games_with_details_data, dict)
        assert "data" in games_with_details_data
        assert isinstance(games_with_details_data["data"], list)
        assert "details" in games_with_details_data["data"][0]


@pytest.mark.asyncio
async def test_get_similar_games_with_details_integration():
    app = FastMCP()
    app.tool(get_games_list.fn)
    app.tool(get_similar_games_with_details.fn)

    async with Client(app) as client:
        list_result = await client.call_tool("get_games_list", {"limit": 1})
        list_data = json.loads(list_result.content[0].text)
        game_id = list_data["data"][0]["id"]

        similar_games_with_details_result = await client.call_tool(
            "get_similar_games_with_details", {"game_id": game_id, "limit": 1}
        )
        similar_games_with_details_data = json.loads(
            similar_games_with_details_result.content[0].text
        )

        assert isinstance(similar_games_with_details_data, dict)
        assert "data" in similar_games_with_details_data
        assert isinstance(similar_games_with_details_data["data"], list)
        assert "details" in similar_games_with_details_data["data"][0]
