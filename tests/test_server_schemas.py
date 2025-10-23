# tests/test_server_schemas.py
import pytest
from inline_snapshot import snapshot

# Import the app from your server.py
from server import app


@pytest.mark.asyncio
async def test_get_game_details_schemas():
    """Verify the schema for the get_game_details tool."""

    # 1. Get the tool from the app
    tool = await app.get_tool("get_game_details")
    assert tool is not None

    # 2. Verify the input schema (Parameters)
    assert tool.parameters == snapshot(
        {
            "properties": {
                "game_slug": {"type": "string"},
                "category": {"type": "string"},
            },
            "required": ["game_slug", "category"],
            "type": "object",
        }
    )

    # 3. Verify the output schema
    assert tool.output_schema == snapshot(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "slug": {"type": "string"},
                "score": {"type": "number"},
                "total_reviews": {"type": "integer"},
                "platform": {"type": "object"},
                "category": {"type": "object"},
                "subcategory": {"type": "object"},
                "categories": {"type": "array"},
                "top_game": {"type": "boolean"},
                "is_minireview_pick": {"type": "boolean"},
                "is_game_of_week": {"type": "boolean"},
                "description": {"type": "string"},
                "review": {"type": "string"},
                "spec": {"type": "array"},
                "tags": {"type": "array"},
            },
        }
    )


@pytest.mark.asyncio
async def test_get_games_list_schemas():
    """Verify the schema for the get_games_list tool."""

    tool = await app.get_tool("get_games_list")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "search": {"type": "string", "default": ""},
                "orderBy": {
                    "$ref": "#/$defs/GamesListOrderBy",
                    "default": "last-added-reviews",
                },
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": [],
                },
                "players": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "network": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "monetization_android": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "monetization_ios": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "screen_orientation": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "category": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "sub_category": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "tags": {"items": {"type": "string"}, "type": "array", "default": []},
                "countries_android": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "countries_ios": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "score": {
                    "additionalProperties": {"type": "integer"},
                    "type": "object",
                    "default": {},
                },
            },
            "type": "object",
            "$defs": {
                "GamesListOrderBy": {
                    "description": (
                        "Represents the available sorting options for game lists."
                    ),
                    "enum": [
                        "last-added-reviews",
                        "last-updated-games",
                        "new-on-minireview",
                        "release-date",
                        "highest-user-ratings",
                        "highest-score",
                        "highest-google-play-score",
                        "highest-appStore-score",
                    ],
                    "type": "string",
                },
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                },
            },
        }
    )

    assert tool.output_schema == snapshot(
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "description": "Game ID"},
                            "name": {"type": "string", "description": "Game Name"},
                            "slug": {
                                "type": "string",
                                "description": "The slug for the game, used in URLs",
                            },
                            "score": {"type": "number"},
                            "total_reviews": {
                                "type": "integer",
                                "description": "Total number of reviews",
                            },
                            "positive_review_percentage": {
                                "type": "number",
                                "description": "Percentage of positive reviews",
                            },
                            "platform": {
                                "type": "object",
                                "properties": {
                                    "android": {"type": "object"},
                                    "ios": {"type": "object"},
                                },
                            },
                            "category": {"type": "object"},
                            "categories": {"type": "array"},
                            "description": {
                                "type": "string",
                                "description": "Game description",
                            },
                            "die_date": {"type": ["string", "null"]},
                            "pick_date": {"type": ["string", "null"]},
                            "week": {"type": ["string", "null"]},
                            "price": {"type": ["string", "number", "null"]},
                        },
                    },
                },
                "current_page": {"type": "integer"},
                "total_pages": {"type": "integer"},
                "is_last_page": {"type": "boolean"},
            },
            "required": ["data", "current_page", "total_pages", "is_last_page"],
        }
    )


@pytest.mark.asyncio
async def test_get_game_ratings_schemas():
    """Verify the schema for the get_game_ratings tool."""

    tool = await app.get_tool("get_game_ratings")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "game_id": {"type": "integer"},
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "type": {
                    "$ref": "#/$defs/GameRatingType",
                    "default": "all",
                },
                "orderBy": {
                    "$ref": "#/$defs/GameRatingsOrderBy",
                    "default": "newest",
                },
            },
            "required": ["game_id"],
            "type": "object",
            "$defs": {
                "GameRatingType": {
                    "description": "Represents the available game rating types.",
                    "enum": ["all", "positive", "negative"],
                    "type": "string",
                },
                "GameRatingsOrderBy": {
                    "description": (
                        "Represents the available sorting options for game ratings."
                    ),
                    "enum": ["newest", "oldest", "most-relevant"],
                    "type": "string",
                },
            },
        }
    )

    assert tool.output_schema == snapshot(
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "date": {"type": "string"},
                            "score": {"type": "number"},
                            "text": {"type": "string"},
                            "type": {"type": "string"},
                        },
                    },
                },
                "current_page": {"type": "integer"},
                "total_ratings": {"type": "integer"},
                "total_positive_ratings": {"type": "integer"},
                "total_negative_ratings": {"type": "integer"},
                "is_last_page": {"type": "boolean"},
                "positive_percentage": {"type": "number"},
            },
        }
    )


@pytest.mark.asyncio
async def test_get_similar_games_schemas():
    """Verify the schema for the get_similar_games tool."""

    tool = await app.get_tool("get_similar_games")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "game_id": {"type": "integer"},
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": [],
                },
            },
            "required": ["game_id"],
            "type": "object",
            "$defs": {
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                }
            },
        }
    )

    assert tool.output_schema == snapshot(
        {
            "type": "object",
            "properties": {"data": {"type": "array", "items": {"type": "object"}}},
        }
    )


@pytest.mark.asyncio
async def test_get_all_filters_schemas():
    """Verify the schema for the get_all_filters tool."""

    tool = await app.get_tool("get_all_filters")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {
            "type": "object",
            "properties": {
                "players": {"type": "object"},
                "network": {"type": "object"},
                "monetization_android": {"type": "object"},
                "monetization_ios": {"type": "object"},
                "screen_orientation": {"type": "object"},
                "category": {"type": "object"},
                "sub_category": {"type": "object"},
                "tags": {"type": "object"},
                "countries_android": {"type": "object"},
                "countries_ios": {"type": "object"},
                "score": {"type": "object"},
            },
        }
    )


@pytest.mark.asyncio
async def test_get_player_options_schemas():
    """Verify the schema for the get_player_options tool."""

    tool = await app.get_tool("get_player_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_network_options_schemas():
    """Verify the schema for the get_network_options tool."""

    tool = await app.get_tool("get_network_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_monetization_android_options_schemas():
    """Verify the schema for the get_monetization_android_options tool."""

    tool = await app.get_tool("get_monetization_android_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_monetization_ios_options_schemas():
    """Verify the schema for the get_monetization_ios_options tool."""

    tool = await app.get_tool("get_monetization_ios_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_screen_orientation_options_schemas():
    """Verify the schema for the get_screen_orientation_options tool."""

    tool = await app.get_tool("get_screen_orientation_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_category_options_schemas():
    """Verify the schema for the get_category_options tool."""

    tool = await app.get_tool("get_category_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_sub_category_options_schemas():
    """Verify the schema for the get_sub_category_options tool."""

    tool = await app.get_tool("get_sub_category_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_tag_options_schemas():
    """Verify the schema for the get_tag_options tool."""

    tool = await app.get_tool("get_tag_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_countries_android_options_schemas():
    """Verify the schema for the get_countries_android_options tool."""

    tool = await app.get_tool("get_countries_android_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_countries_ios_options_schemas():
    """Verify the schema for the get_countries_ios_options tool."""

    tool = await app.get_tool("get_countries_ios_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_score_options_schemas():
    """Verify the schema for the get_score_options tool."""

    tool = await app.get_tool("get_score_options")
    assert tool is not None

    assert tool.parameters == snapshot({"properties": {}, "type": "object"})

    assert tool.output_schema == snapshot(
        {"type": "object", "properties": {"options": {"type": "object"}}}
    )


@pytest.mark.asyncio
async def test_get_home_schemas():
    """Verify the schema for the get_home tool."""

    tool = await app.get_tool("get_home")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "page": {"type": "integer", "default": 1},
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": ["android", "ios"],
                },
                "ids_ignore": {
                    "items": {"type": "integer"},
                    "type": "array",
                    "default": [],
                },
                "orderBy": {
                    "$ref": "#/$defs/GamesListOrderBy",
                    "default": "last-added-reviews",
                },
            },
            "type": "object",
            "$defs": {
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                },
                "GamesListOrderBy": {
                    "description": (
                        "Represents the available sorting options for game lists."
                    ),
                    "enum": [
                        "last-added-reviews",
                        "last-updated-games",
                        "new-on-minireview",
                        "release-date",
                        "highest-user-ratings",
                        "highest-score",
                        "highest-google-play-score",
                        "highest-appStore-score",
                    ],
                    "type": "string",
                },
            },
        }
    )

    assert tool.output_schema == snapshot(
        {"additionalProperties": True, "type": "object"}
    )


@pytest.mark.asyncio
async def test_get_games_of_the_week_schemas():
    """Verify the schema for the get_games_of_the_week tool."""

    tool = await app.get_tool("get_games_of_the_week")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": ["android", "ios"],
                },
                "players": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "network": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "monetization_android": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "monetization_ios": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "screen_orientation": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "category": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "sub_category": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "tags": {"items": {"type": "string"}, "type": "array", "default": []},
                "countries_android": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "countries_ios": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "score": {
                    "additionalProperties": {"type": "integer"},
                    "type": "object",
                    "default": {},
                },
            },
            "type": "object",
            "$defs": {
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                }
            },
        }
    )

    assert tool.output_schema == snapshot(
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "description": "Game ID"},
                            "name": {"type": "string", "description": "Game Name"},
                            "slug": {
                                "type": "string",
                                "description": "The slug for the game, used in URLs",
                            },
                            "score": {"type": "number"},
                            "total_reviews": {
                                "type": "integer",
                                "description": "Total number of reviews",
                            },
                            "positive_review_percentage": {
                                "type": "number",
                                "description": "Percentage of positive reviews",
                            },
                            "platform": {
                                "type": "object",
                                "properties": {
                                    "android": {"type": "object"},
                                    "ios": {"type": "object"},
                                },
                            },
                            "category": {"type": "object"},
                            "categories": {"type": "array"},
                            "description": {
                                "type": "string",
                                "description": "Game description",
                            },
                            "die_date": {"type": ["string", "null"]},
                            "pick_date": {"type": ["string", "null"]},
                            "week": {"type": ["string", "null"]},
                            "price": {"type": ["string", "number", "null"]},
                        },
                    },
                },
                "current_page": {"type": "integer"},
                "total_pages": {"type": "integer"},
                "is_last_page": {"type": "boolean"},
            },
            "required": ["data", "current_page", "total_pages", "is_last_page"],
        }
    )


@pytest.mark.asyncio
async def test_get_minireview_pick_schemas():
    """Verify the schema for the get_minireview_pick tool."""

    tool = await app.get_tool("get_minireview_pick")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": ["android", "ios"],
                },
                "players": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "network": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "monetization_android": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "monetization_ios": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "screen_orientation": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "category": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "sub_category": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "tags": {"items": {"type": "string"}, "type": "array", "default": []},
                "countries_android": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "countries_ios": {
                    "items": {"type": "string"},
                    "type": "array",
                    "default": [],
                },
                "score": {
                    "additionalProperties": {"type": "integer"},
                    "type": "object",
                    "default": {},
                },
            },
            "type": "object",
            "$defs": {
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                }
            },
        }
    )

    assert tool.output_schema == snapshot(
        {"additionalProperties": True, "type": "object"}
    )


@pytest.mark.asyncio
async def test_get_top_user_ratings_schemas():
    """Verify the schema for the get_top_user_ratings tool."""

    tool = await app.get_tool("get_top_user_ratings")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "orderBy": {
                    "$ref": "#/$defs/TopUserRatingsOrderBy",
                    "default": "this-week",
                },
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": ["android", "ios"],
                },
            },
            "type": "object",
            "$defs": {
                "TopUserRatingsOrderBy": {
                    "description": (
                        "Represents the available sorting options for top user ratings."
                    ),
                    "enum": ["this-week", "this-month", "all-time"],
                    "type": "string",
                },
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                },
            },
        }
    )

    assert tool.output_schema == snapshot(
        {"additionalProperties": True, "type": "object"}
    )


@pytest.mark.asyncio
async def test_get_upcoming_games_schemas():
    """Verify the schema for the get_upcoming_games tool."""

    tool = await app.get_tool("get_upcoming_games")
    assert tool is not None

    assert tool.parameters == snapshot(
        {
            "properties": {
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 50},
                "orderBy": {
                    "$ref": "#/$defs/GamesListOrderBy",
                    "default": "release-date",
                },
                "platforms": {
                    "items": {"$ref": "#/$defs/Platform"},
                    "type": "array",
                    "default": ["android", "ios"],
                },
            },
            "type": "object",
            "$defs": {
                "GamesListOrderBy": {
                    "description": (
                        "Represents the available sorting options for game lists."
                    ),
                    "enum": [
                        "last-added-reviews",
                        "last-updated-games",
                        "new-on-minireview",
                        "release-date",
                        "highest-user-ratings",
                        "highest-score",
                        "highest-google-play-score",
                        "highest-appStore-score",
                    ],
                    "type": "string",
                },
                "Platform": {
                    "description": "Represents the available platforms.",
                    "enum": ["android", "ios"],
                    "type": "string",
                },
            },
        }
    )

    assert tool.output_schema == snapshot(
        {"additionalProperties": True, "type": "object"}
    )
