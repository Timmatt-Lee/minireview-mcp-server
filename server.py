from fastmcp import FastMCP

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    GameRatingsOrderBy,
    GameRatingType,
    GamesListOrderBy,
    Platform,
    TopUserRatingsOrderBy,
)

app = FastMCP()
client = MiniReviewClient()


@app.tool(
    title="Fetch Games List",
    description=(
        "Fetches a paginated list of games with extensive filtering and sorting "
        "capabilities. IMPORTANT: Filter parameters must use values obtained from the "
        "corresponding `get_*_options` functions."
    ),
    output_schema={
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
    },
)
def get_games_list(
    page: int = 1,
    limit: int = 50,
    search: str = "",
    orderBy: GamesListOrderBy = GamesListOrderBy.LAST_ADDED_REVIEWS,
    platforms: list[Platform] = [],
    players: list[str] = [],
    network: list[str] = [],
    monetization_android: list[str] = [],
    monetization_ios: list[str] = [],
    screen_orientation: list[str] = [],
    category: list[str] = [],
    sub_category: list[str] = [],
    tags: list[str] = [],
    countries_android: list[str] = [],
    countries_ios: list[str] = [],
    score: dict[str, int] = {},
) -> dict:
    """
    Fetches a list of games from the MiniReview database with extensive filtering
    capabilities.

    Args:
        page: The page number to fetch.
        limit: The number of games to fetch per page.
        search: A search query to filter games by name.
        orderBy: The sorting order for the games list.
        platforms: A list of platforms to filter by (e.g., 'android', 'ios').
        players: A list of player modes to filter by. Must be values from
            `get_player_options`.
        network: The network availability to filter by. Must be values from
            `get_network_options`.
        monetization_android: A list of monetization models for Android. Must be
            values from `get_monetization_android_options`.
        monetization_ios: A list of monetization models for iOS. Must be values
            from `get_monetization_ios_options`.
        screen_orientation: The screen orientation to filter by. Must be values
            from `get_screen_orientation_options`.
        category: The game category to filter by. Must be values from
            `get_category_options`.
        sub_category: The game sub-category to filter by. Must be values from
            `get_sub_category_options`.
        tags: A list of tags to filter by. Must be values from `get_tag_options`.
        countries_android: A list of countries for Android games. Must be values
            from `get_countries_android_options`.
        countries_ios: A list of countries for iOS games. Must be values from
            `get_countries_ios_options`.
        score: A dictionary to filter by score.

    Returns:
        A dictionary containing a list of games and pagination information.
    """
    games_list_res = client.get_games_list(
        page=page,
        limit=limit,
        orderBy=orderBy,
        platforms=platforms,
        players=players,
        network=network,
        monetization_android=monetization_android,
        monetization_ios=monetization_ios,
        screen_orientation=screen_orientation,
        category=category,
        sub_category=sub_category,
        tags=tags,
        countries_android=countries_android,
        countries_ios=countries_ios,
        score=score,
    )

    games_list_data = [
        {
            "id": game_list_data_item.get("id"),
            "name": game_list_data_item.get("nome"),
            "slug": game_list_data_item.get("slug"),
            "score": game_list_data_item.get("nota"),
            "total_reviews": game_list_data_item.get("avaliacoes_total"),
            "positive_review_percentage": game_list_data_item.get(
                "avaliacoes_positivas_porcento"
            ),
            "platform": {
                "android": {
                    "is_available": game_list_data_item.get("disponivel_android"),
                },
                "ios": {
                    "is_available": game_list_data_item.get("disponivel_ios"),
                },
            },
            "category": game_list_data_item.get("categoria"),
            "categories": game_list_data_item.get("categorias"),
            "description": game_list_data_item.get("descricao"),
            "die_date": game_list_data_item.get("morto_data"),
            "pick_date": game_list_data_item.get("pick_data"),
            "week": game_list_data_item.get("semana"),
            "price": game_list_data_item.get("price"),
        }
        for game_list_data_item in games_list_res.get("data")
    ]

    return {
        "data": games_list_data,
        "current_page": games_list_res.get("page"),
        "total_pages": games_list_res.get("total"),
        "is_last_page": games_list_res.get("ultima_pagina"),
    }


@app.tool(
    title="Get Game Details",
    description=(
        "Fetches detailed information for a single game by its slug and category."
    ),
    output_schema={
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
    },
)
def get_game_details(game_slug: str, category: str) -> dict:
    """
    Fetches detailed information for a specific game.

    Args:
        game_slug: The slug of the game (e.g., 'seven-knights-idle-adventure').
        category: The category of the game.

    Returns:
        A dictionary containing the details of the.
    """
    game_details = client.get_game_details(game_slug, category)
    game_details_data = game_details.get("data")

    return {
        "id": game_details_data.get("id"),
        "name": game_details_data.get("nome"),
        "slug": game_details_data.get("slug"),
        "score": game_details_data.get("nota"),
        "total_reviews": game_details_data.get("total_avaliacoes"),
        "platform": {
            "android": {
                "is_available": game_details_data.get("disponivel_android"),
                "price": game_details_data.get("preco_android"),
                "is_dead": game_details_data.get("android_morto"),
                "dead_date": game_details_data.get("android_morto_data"),
                "link": game_details_data.get("link_android"),
            },
            "ios": {
                "is_available": game_details_data.get("disponivel_ios"),
                "price": game_details_data.get("preco_ios"),
                "is_dead": game_details_data.get("ios_morto"),
                "dead_date": game_details_data.get("ios_morto_data"),
                "link": game_details_data.get("link_ios"),
            },
        },
        "category": game_details_data.get("categoria"),
        "subcategory": game_details_data.get("subcategoria"),
        "categories": game_details_data.get("categorias"),
        "top_game": game_details_data.get("top_game"),
        "is_minireview_pick": game_details_data.get("our_picks"),
        "is_game_of_week": game_details_data.get("game_of_the_week"),
        "description": game_details_data.get("descricao"),
        "review": game_details_data.get("review"),
        "spec": game_details_data.get("especificacoes"),
        "tags": game_details_data.get("tags"),
    }


@app.tool(
    title="Get Game Ratings",
    description="Fetches a list of user ratings for a specific game.",
    output_schema={
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
    },
)
def get_game_ratings(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    type: GameRatingType = GameRatingType.ALL,
    orderBy: GameRatingsOrderBy = GameRatingsOrderBy.NEWEST,
) -> dict:
    """
    Fetches the ratings for a specific game.

    Args:
        game_id: The ID of the game.
        page: The page number to fetch.
        limit: The number of ratings to fetch per page.
        type: The type of ratings to fetch.
        orderBy: The sorting order for the ratings.

    Returns:
        A dictionary containing a list of ratings and pagination information.
    """
    game_ratings_res = client.get_game_ratings(game_id, page, limit, type, orderBy)

    game_rating_data = [
        {
            "id": game_ratings_data_item.get("id"),
            "date": game_ratings_data_item.get("data"),
            "score": game_ratings_data_item.get("pontuacao"),
            "text": game_ratings_data_item.get("texto"),
            "type": game_ratings_data_item.get("tipo"),
        }
        for game_ratings_data_item in game_ratings_res.get("data")
    ]

    return {
        "data": game_rating_data,
        "current_page": game_ratings_res.get("page"),
        "total_ratings": game_ratings_res.get("total"),
        "total_positive_ratings": game_ratings_res.get("total_positivo"),
        "total_negative_ratings": game_ratings_res.get("total_negativo"),
        "is_last_page": game_ratings_res.get("ultima_pagina"),
        "positive_percentage": game_ratings_res.get("porcento"),
    }


@app.tool(
    title="Get Similar Games",
    description="Fetches a list of games similar to a specific game.",
    output_schema={
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
    },
)
def get_similar_games(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    platforms: list[Platform] = [],
) -> dict:
    """
    Fetches a list of games similar to a specific game.

    Args:
        game_id: The ID of the game to find similar games for.
        page: The page number to fetch.
        limit: The number of similar games to fetch per page.
        platforms: A list of platforms to filter by.
        orderBy: The sorting order for the similar games list.

    Returns:
        A dictionary containing a list of similar games and pagination information.
    """
    return client.get_similar_games(game_id, page, limit, platforms)


@app.tool(
    title="Get All Filters",
    description=(
        "Fetches all available filter options for games, such as categories, tags, "
        "etc. For specific filters, consider using the more granular `get_*_options` "
        "functions."
    ),
    output_schema={
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
    },
)
def get_all_filters() -> dict:
    """
    Fetches all available filter options for games, such as categories, tags,
    and monetization types.

    Returns:
        A dictionary containing all available filter options.
    """
    return {
        "players": client.get_players(),
        "network": client.get_network_options(),
        "monetization_android": client.get_monetization_android(),
        "monetization_ios": client.get_monetization_ios(),
        "screen_orientation": client.get_screen_orientation_options(),
        "category": client.get_category_options(),
        "sub_category": client.get_sub_category_options(),
        "tags": client.get_tags(),
        "countries_android": client.get_countries_android(),
        "countries_ios": client.get_countries_ios(),
        "score": client.get_score_options(),
    }


@app.tool(
    title="Get Player Options",
    description=(
        "Fetches all available player mode filter options (e.g., 'singleplayer')."
    ),
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_player_options() -> dict:
    """Fetches available player mode options."""
    return {"options": client.get_players()}


@app.tool(
    title="Get Network Options",
    description=(
        "Fetches all available network mode filter options (e.g., 'online', 'offline')."
    ),
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_network_options() -> dict:
    """Fetches available network options."""
    return {"options": client.get_network_options()}


@app.tool(
    title="Get Android Monetization Options",
    description=(
        "Fetches all available monetization filter options for the Android platform."
    ),
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_monetization_android_options() -> dict:
    """Fetches available monetization options for Android."""
    return {"options": client.get_monetization_android()}


@app.tool(
    title="Get iOS Monetization Options",
    description=(
        "Fetches all available monetization filter options for the iOS platform."
    ),
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_monetization_ios_options() -> dict:
    """Fetches available monetization options for iOS."""
    return {"options": client.get_monetization_ios()}


@app.tool(
    title="Get Screen Orientation Options",
    description="Fetches all available screen orientation filter options.",
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_screen_orientation_options() -> dict:
    """Fetches available screen orientation options."""
    return {"options": client.get_screen_orientation_options()}


@app.tool(
    title="Get Category Options",
    description="Fetches all available main game category filter options.",
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_category_options() -> dict:
    """Fetches available category options."""
    return {"options": client.get_category_options()}


@app.tool(
    title="Get Sub-Category Options",
    description="Fetches all available game sub-category filter options.",
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_sub_category_options() -> dict:
    """Fetches available sub-category options."""
    return {"options": client.get_sub_category_options()}


@app.tool(
    title="Get Tag Options",
    description="Fetches all available game tag filter options.",
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_tag_options() -> dict:
    """Fetches available tag options."""
    return {"options": client.get_tags()}


@app.tool(
    title="Get Android Country Options",
    description=(
        "Fetches all available country/region filter options for the Android platform."
    ),
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_countries_android_options() -> dict:
    """Fetches available country options for Android."""
    return {"options": client.get_countries_android()}


@app.tool(
    title="Get iOS Country Options",
    description=(
        "Fetches all available country/region filter options for the iOS platform."
    ),
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_countries_ios_options() -> dict:
    """Fetches available country options for iOS."""
    return {"options": client.get_countries_ios()}


@app.tool(
    title="Get Score Options",
    description="Fetches all available score filter options.",
    output_schema={
        "type": "object",
        "properties": {"options": {"type": "object"}},
    },
)
def get_score_options() -> dict:
    """Fetches available score options."""
    return {"options": client.get_score_options()}


@app.tool(
    title="Get Home Page Content",
    description=(
        "Fetches the content for the home page, which typically includes a mix of "
        "different game lists."
    ),
)
def get_home(
    page: int = 1,
    platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    ids_ignore: list[int] = [],
    orderBy: GamesListOrderBy = GamesListOrderBy.LAST_ADDED_REVIEWS,
) -> dict:
    """
    Fetches the home page content.

    Args:
        page: The page number to fetch.
        platforms: A list of platforms to filter by.
        ids_ignore: A list of game IDs to ignore.
        orderBy: The sorting order for the games list.

    Returns:
        A dictionary containing the home page content.
    """
    return client.get_home(page, platforms, ids_ignore, orderBy)


@app.tool(
    title="Get Games of the Week",
    description="Fetches a list of games featured as 'Game of the Week'.",
    output_schema={
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
    },
)
def get_games_of_the_week(
    page: int = 1,
    limit: int = 50,
    platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    players: list[str] = [],
    network: list[str] = [],
    monetization_android: list[str] = [],
    monetization_ios: list[str] = [],
    screen_orientation: list[str] = [],
    category: list[str] = [],
    sub_category: list[str] = [],
    tags: list[str] = [],
    countries_android: list[str] = [],
    countries_ios: list[str] = [],
    score: dict[str, int] = {},
) -> dict:
    """
    Fetches games of the week.

    Args:
        page: The page number to fetch.
        limit: The number of games to fetch per page.
        platforms: A list of platforms to filter by.
        players: A list of player modes to filter by.
        network: The network availability to filter by.
        monetization_android: A list of monetization models for Android to filter by.
        monetization_ios: A list of monetization models for iOS to filter by.
        screen_orientation: The screen orientation to filter by.
        category: The game category to filter by.
        sub_category: The game sub-category to filter by.
        tags: A list of tags to filter by.
        countries_android: A list of countries to filter by for Android games.
        countries_ios: A list of countries to filter by for iOS games.
        score: A dictionary to filter by score.

    Returns:
        A dictionary containing a list of games of the week.
    """
    get_games_of_the_week_res = client.get_games_of_the_week(
        page=page,
        limit=limit,
        platforms=platforms,
        players=players,
        network=network,
        monetization_android=monetization_android,
        monetization_ios=monetization_ios,
        screen_orientation=screen_orientation,
        category=category,
        sub_category=sub_category,
        tags=tags,
        countries_android=countries_android,
        countries_ios=countries_ios,
        score=score,
    )

    get_games_of_the_week_data = [
        {
            "id": get_games_of_the_week_data_item.get("id"),
            "name": get_games_of_the_week_data_item.get("nome"),
            "slug": get_games_of_the_week_data_item.get("slug"),
            "score": get_games_of_the_week_data_item.get("nota"),
            "total_reviews": get_games_of_the_week_data_item.get("avaliacoes_total"),
            "positive_review_percentage": get_games_of_the_week_data_item.get(
                "avaliacoes_positivas_porcento"
            ),
            "platform": {
                "android": {
                    "is_available": get_games_of_the_week_data_item.get(
                        "disponivel_android"
                    ),
                },
                "ios": {
                    "is_available": get_games_of_the_week_data_item.get(
                        "disponivel_ios"
                    ),
                },
            },
            "category": get_games_of_the_week_data_item.get("categoria"),
            "categories": get_games_of_the_week_data_item.get("categorias"),
            "description": get_games_of_the_week_data_item.get("descricao"),
            "die_date": get_games_of_the_week_data_item.get("morto_data"),
            "pick_date": get_games_of_the_week_data_item.get("pick_data"),
            "week": get_games_of_the_week_data_item.get("semana"),
            "price": get_games_of_the_week_data_item.get("price"),
        }
        for get_games_of_the_week_data_item in get_games_of_the_week_res.get("data")
    ]

    return {
        "data": get_games_of_the_week_data,
        "current_page": get_games_of_the_week_res.get("page"),
        "total_pages": get_games_of_the_week_res.get("total"),
        "is_last_page": get_games_of_the_week_res.get("ultima_pagina"),
    }


@app.tool(
    title="Get MiniReview Picks",
    description="Fetches games that are specially selected as 'MiniReview Picks'.",
)
def get_minireview_pick(
    page: int = 1,
    limit: int = 50,
    platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    players: list[str] = [],
    network: list[str] = [],
    monetization_android: list[str] = [],
    monetization_ios: list[str] = [],
    screen_orientation: list[str] = [],
    category: list[str] = [],
    sub_category: list[str] = [],
    tags: list[str] = [],
    countries_android: list[str] = [],
    countries_ios: list[str] = [],
    score: dict[str, int] = {},
) -> dict:
    """
    Fetches games that are MiniReview picks.

    Args:
        page: The page number to fetch.
        limit: The number of games to fetch per page.
        platforms: A list of platforms to filter by.
        players: A list of player modes to filter by.
        network: The network availability to filter by.
        monetization_android: A list of monetization models for Android to filter by.
        monetization_ios: A list of monetization models for iOS to filter by.
        screen_orientation: The screen orientation to filter by.
        category: The game category to filter by.
        sub_category: The game sub-category to filter by.
        tags: A list of tags to filter by.
        countries_android: A list of countries to filter by for Android games.
        countries_ios: A list of countries to filter by for iOS games.
        score: A dictionary to filter by score.

    Returns:
        A dictionary containing a list of MiniReview picks.
    """
    return client.get_minireview_pick(
        page=page,
        limit=limit,
        platforms=platforms,
        players=players,
        network=network,
        monetization_android=monetization_android,
        monetization_ios=monetization_ios,
        screen_orientation=screen_orientation,
        category=category,
        sub_category=sub_category,
        tags=tags,
        countries_android=countries_android,
        countries_ios=countries_ios,
        score=score,
    )


@app.tool(
    title="Get Top User-Rated Games",
    description=(
        "Fetches a list of games with the top user ratings, sortable by period "
        "(e.g., this week, this month, all time)."
    ),
)
def get_top_user_ratings(
    page: int = 1,
    limit: int = 50,
    orderBy: TopUserRatingsOrderBy = TopUserRatingsOrderBy.THIS_WEEK,
    platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
) -> dict:
    """
    Fetches top user ratings.

    Args:
        page: The page number to fetch.
        limit: The number of ratings to fetch per page.
        orderBy: The sorting order for the ratings.
        platforms: A list of platforms to filter by.

    Returns:
        A dictionary containing a list of top user-rated games.
    """
    return client.get_top_user_ratings(page, limit, orderBy, platforms)


@app.tool(
    title="Get Upcoming Games",
    description="Fetches a list of games that are scheduled for future release.",
)
def get_upcoming_games(
    page: int = 1,
    limit: int = 50,
    orderBy: GamesListOrderBy = GamesListOrderBy.RELEASE_DATE,
    platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
) -> dict:
    """
    Fetches upcoming games.

    Args:
        page: The page number to fetch.
        limit: The number of games to fetch per page.
        orderBy: The sorting order for the games list.
        platforms: A list of platforms to filter by.

    Returns:
        A dictionary containing a list of upcoming games.
    """
    return client.get_upcoming_games(page, limit, orderBy, platforms)


if __name__ == "__main__":
    app.run()
