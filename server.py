from fastmcp import FastMCP

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    GameRatingsOrderBy,
    GameRatingType,
    GamesListOrderBy,
    Platform,
)

app = FastMCP()
client = MiniReviewClient()


@app.tool(description="Fetches a list of games with extensive filtering capabilities.")
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
        players: A list of player modes to filter by
            (e.g., 'singleplayer', 'multiplayer').
        network: The network availability to filter by (e.g., 'online', 'offline').
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
            "week": game_list_data_item.get("pick_data"),
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


@app.tool(description="Fetches detailed information for a specific game.")
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


@app.tool(description="Fetches the ratings for a specific game.")
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


@app.tool(description="Fetches a list of games similar to a specific game.")
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
    description=(
        "Fetches a list of games with extensive filtering capabilities and then "
        "fetches the details for each game in the list."
    )
)
def get_games_list_with_details(
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
    Fetches a list of games with extensive filtering capabilities and then fetches
    the details for each game in the list.

    This is a convenience function that combines `get_games_list` and
    `get_game_details`.

    Args:
        page: The page number to fetch.
        limit: The number of games to fetch per page.
        search: A search query to filter games by name.
        orderBy: The sorting order for the games list.
        platforms: A list of platforms to filter by (e.g., 'android', 'ios').
        players: A list of player modes to filter by
            (e.g., 'singleplayer', 'multiplayer').
        network: The network availability to filter by (e.g., 'online', 'offline').
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
        A dictionary containing a list of games with their details and pagination
        information.
    """
    games = client.get_games_list(
        page=page,
        limit=limit,
        search=search,
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
    for game in games["data"]:
        game["details"] = client.get_game_details(
            game["slug"], game["categoria"]["slug"]
        )
    return games


@app.tool(
    description=(
        "Fetches a list of games similar to a specific game and then fetches the "
        "details for each game in the list."
    )
)
def get_similar_games_with_details(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    platforms: list[Platform] = [],
) -> dict:
    """
    Fetches a list of games similar to a specific game and then fetches the
    details for each game in the list.

    This is a convenience function that combines `get_similar_games` and
    `get_game_details`.

    Args:
        game_id: The ID of the game to find similar games for.
        page: The page number to fetch.
        limit: The number of similar games to fetch per page.
        platforms: A list of platforms to filter by.
        orderBy: The sorting order for the similar games list.

    Returns:
        A dictionary containing a list of similar games with their details and
        pagination information.
    """
    games = client.get_similar_games(game_id, page, limit, platforms)
    for game in games["data"]:
        game["details"] = client.get_game_details(
            game["slug"], game["categoria"]["slug"]
        )
    return games


if __name__ == "__main__":
    app.run()
