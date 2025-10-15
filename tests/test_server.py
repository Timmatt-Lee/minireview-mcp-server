import pytest
import json
from unittest.mock import MagicMock, patch
from fastmcp import FastMCP, Client
from server import (
    get_games_list,
    get_game_details,
    get_game_ratings,
    get_similar_games,
    get_collections,
    get_categories,
    get_games_list_with_details,
    get_similar_games_with_details,
)

@pytest.fixture
def mock_minireview_client():
    mock_client = MagicMock()
    mock_client.get_games_list.return_value = {
        "results": [
            {"id": 1, "name": "Game 1", "slug": "game-1", "category": "action"},
            {"id": 2, "name": "Game 2", "slug": "game-2", "category": "adventure"},
        ],
        "pagination": {"page": 1, "limit": 2, "total": 2},
        "filtros": "some_filter_data"
    }
    mock_client.get_game_details.return_value = {"id": 1, "name": "Test Game", "slug": "test-slug"}
    mock_client.get_game_ratings.return_value = {"results": [{"rating": 5}]}
    mock_client.get_similar_games.return_value = {"results": [{"id": 3, "name": "Similar Game", "slug": "similar-game", "category": "action"}]}
    mock_client.get_collections.return_value = {"results": [{"name": "Collection 1"}]}
    mock_client.get_categories.return_value = {"results": [{"name": "Category 1"}]}
    return mock_client



@pytest.mark.asyncio
async def test_get_game_details(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_game_details.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_game_details", {"game_slug": "test-slug", "category": "test-category"})
            data = json.loads(result.content[0].text)

            assert data == {
                "id": 1,
                "name": "Test Game",
                "total_review": None,
                "positive_review_percentage": None,
                "score": None,
                "favorite_user": None,
                "category": None,
                "subcategory": None,
                "available_platforms": {
                    "android": None,
                    "ios": None,
                },
                "description": None,
                "die_date": None,
                "pick_date": None,
                "week": None,
                "price": None,
            }

@pytest.mark.asyncio
async def test_get_game_ratings(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_game_ratings.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_game_ratings", {"game_id": 1})
            data = json.loads(result.content[0].text)

            assert data == {"results": [{"rating": 5}]}

@pytest.mark.asyncio
async def test_get_similar_games(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_similar_games.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_similar_games", {"game_id": 1})
            data = json.loads(result.content[0].text)

            assert data == {"results": [{"id": 3, "name": "Similar Game", "slug": "similar-game", "category": "action"}]}

@pytest.mark.asyncio
async def test_get_collections(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_collections.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_collections", {})
            data = json.loads(result.content[0].text)

            assert data == {"results": [{"name": "Collection 1"}]}

@pytest.mark.asyncio
async def test_get_categories(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_categories.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_categories", {})
            data = json.loads(result.content[0].text)

            assert data == {"results": [{"name": "Category 1"}]}

@pytest.mark.asyncio
async def test_get_games_list_with_details(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_games_list_with_details.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_games_list_with_details", {})
            data = json.loads(result.content[0].text)

            assert "details" in data["results"][0]

@pytest.mark.asyncio
async def test_get_game_details_trims_and_translates_response(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        mock_minireview_client.get_game_details.return_value = {
            "id": 1,
            "nome": "Test Game",
            "slug": "test-slug",
            "nota": 4.5,
            "categoria": {"nome": "Aventura"},
            "sub_categoria": "RPG",
            "descricao": "A great game",
            "morto_data": "2025-12-31",
            "data_escolha": "2025-10-15",
            "semana": 42,
            "preco": 10,
            "avaliacoes_total": 100,
            "porcentagem_positiva": 95,
            "usuario_favorito": True,
            "disponivel_android": True,
            "disponivel_ios": False,
            "some_other_field": "should be removed"
        }

        app = FastMCP()
        app.tool(get_game_details.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_game_details", {"game_slug": "test-slug", "category": "test-category"})
            data = json.loads(result.content[0].text)

            expected_data = {
                "id": 1,
                "name": "Test Game",
                "total_review": 100,
                "positive_review_percentage": 95,
                "score": 4.5,
                "favorite_user": True,
                "category": {"name": "Aventura"},
                "subcategory": "RPG",
                "available_platforms": {
                    "android": True,
                    "ios": False,
                },
                "description": "A great game",
                "die_date": "2025-12-31",
                "pick_date": "2025-10-15",
                "week": 42,
                "price": 10,
            }

            assert data == expected_data

@pytest.mark.asyncio
async def test_get_similar_games_with_details(mock_minireview_client):
    with patch('server.MiniReviewClient', return_value=mock_minireview_client):
        app = FastMCP()
        app.tool(get_similar_games_with_details.fn)

        async with Client(app) as client:
            result = await client.call_tool("get_similar_games_with_details", {"game_id": 1})
            data = json.loads(result.content[0].text)

            assert "details" in data["results"][0]