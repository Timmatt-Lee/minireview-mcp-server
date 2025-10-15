import pytest
import json
from fastmcp import FastMCP, Client
from server import get_games_list, get_game_details

@pytest.mark.asyncio
async def test_get_game_details_integration():
    app = FastMCP()
    app.tool(get_games_list.fn)
    app.tool(get_game_details.fn)

    async with Client(app) as client:
        # First, get a list of games to find a valid game to test with
        list_result = await client.call_tool("get_games_list", {"limit": 1})
        list_data = json.loads(list_result.content[0].text)

        assert isinstance(list_data, dict)
        assert "data" in list_data
        assert isinstance(list_data["data"], list)
        assert len(list_data["data"]) > 0

        # Get the first game from the list
        game = list_data["data"][0]
        game_slug = game["slug"]
        category_slug = game["categoria"]["slug"]

        # Now, call get_game_details with the real data
        details_result = await client.call_tool("get_game_details", {"game_slug": game_slug, "category": category_slug})
        details_data = json.loads(details_result.content[0].text)

        # Assert the structure of the trimmed and translated response
        assert isinstance(details_data, dict)
        assert "id" in details_data
        assert "name" in details_data
        assert "slug" not in details_data # Should be removed
        assert "score" in details_data
        assert "category" in details_data
        assert "subcategory" in details_data
        assert "available_platforms" in details_data
        assert "android" in details_data["available_platforms"]
        assert "ios" in details_data["available_platforms"]