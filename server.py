from fastmcp import FastMCP

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    CollectionsOrderBy,
    GameRatingsOrderBy,
    OrderBy,
    Platform,
)

app = FastMCP()


@app.tool(description="Fetches a list of games with extensive filtering capabilities.")
def get_games_list(
    page: int = 1,
    limit: int = 50,
    search: str = "",
    orderBy: OrderBy = OrderBy.LAST_ADDED_REVIEWS,
    platforms: list[Platform] | None = None,
    players: list[str] | None = None,
    network: str | None = None,
    monetization_android: list[str] | None = None,
    monetization_ios: list[str] | None = None,
    screen_orientation: str | None = None,
    category: str | None = None,
    sub_category: str | None = None,
    tags: list[str] | None = None,
    countries_android: list[str] | None = None,
    countries_ios: list[str] | None = None,
    score: dict[str, int] | None = None,
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
    client = MiniReviewClient()
    return client.get_games_list(
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


@app.tool(description="Fetches detailed information for a specific game.")
def get_game_details(game_slug: str, category: str) -> dict:
    """
    Fetches detailed information for a specific game.

    Args:
        game_slug: The slug of the game (e.g., 'seven-knights-idle-adventure').
        category: The category of the game.

    Returns:
        A dictionary containing the details of the game.
    """
    client = MiniReviewClient()
    game_details = client.get_game_details(game_slug, category)

    TRANSLATION_MAP = {
        "nome": "name",
        "avaliacoes_total": "total_reviews",
        "usuario_favorito": "user_favorite",
        "categoria": "category",
        "sub_categoria": "subcategory",
        "filtros": "filters",
        "tipo": "type",
        "ultima_pagina": "last_page",
        "nota": "score",
        "morto_data": "die_date",
        "descricao": "description",
        "preco": "price",
        "semana": "week",
        "data_lancamento": "release_date",
        "data_escolha": "pick_date",
        "porcentagem_positiva": "positive_review_percentage",
        "total_review": "total_review",
        "disponivel_android": "available_android",
        "disponivel_ios": "available_ios",
        "pagina": "page",
        "total": "total",
        "resultados": "results",
        "id": "id",
        "slug": "slug",
    }

    def translate_keys(obj, translation_map):
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                new_key = translation_map.get(k, k)
                new_obj[new_key] = translate_keys(v, translation_map)
            return new_obj
        elif isinstance(obj, list):
            return [translate_keys(item, translation_map) for item in obj]
        else:
            return obj

    translated_details = translate_keys(game_details, TRANSLATION_MAP)

    trimmed_game = {
        "id": translated_details.get("id"),
        "name": translated_details.get("name"),
        "total_review": translated_details.get("total_reviews"),
        "positive_review_percentage": translated_details.get("positive_review_percentage"),
        "score": translated_details.get("score"),
        "favorite_user": translated_details.get("user_favorite"),
        "category": translated_details.get("category"),
        "subcategory": translated_details.get("subcategory"),
        "available_platforms": {
            "android": translated_details.get("available_android"),
            "ios": translated_details.get("available_ios"),
        },
        "description": translated_details.get("description"),
        "die_date": translated_details.get("die_date"),
        "pick_date": translated_details.get("pick_date"),
        "week": translated_details.get("week"),
        "price": translated_details.get("price"),
    }

    return trimmed_game


@app.tool(description="Fetches the ratings for a specific game.")
def get_game_ratings(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    orderBy: GameRatingsOrderBy = GameRatingsOrderBy.NEWEST,
) -> dict:
    """
    Fetches the ratings for a specific game.

    Args:
        game_id: The ID of the game.
        page: The page number to fetch.
        limit: The number of ratings to fetch per page.
        orderBy: The sorting order for the ratings.

    Returns:
        A dictionary containing a list of ratings and pagination information.
    """
    client = MiniReviewClient()
    return client.get_game_ratings(game_id, page, limit, orderBy)


@app.tool(description="Fetches a list of games similar to a specific game.")
def get_similar_games(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    platforms: list[Platform] | None = None,
    orderBy: OrderBy = OrderBy.MOST_POPULAR,
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
    client = MiniReviewClient()
    return client.get_similar_games(game_id, page, limit, platforms, orderBy)


@app.tool(description="Fetches a list of game collections.")
def get_collections(
    page: int = 1,
    limit: int = 50,
    search: str = "",
    orderBy: CollectionsOrderBy = CollectionsOrderBy.MOST_POPULAR,
    loadNew: bool = True,
    loadLastUpdated: bool = True,
) -> dict:
    """
    Fetches a list of game collections.

    Args:
        page: The page number to fetch.
        limit: The number of collections to fetch per page.
        search: A search query to filter collections by name.
        orderBy: The sorting order for the collections list.
        loadNew: Whether to load new collections.
        loadLastUpdated: Whether to load last updated collections.

    Returns:
        A dictionary containing a list of collections and pagination information.
    """
    client = MiniReviewClient()
    return client.get_collections(
        page, limit, search, orderBy, loadNew, loadLastUpdated
    )


@app.tool(description="Fetches a list of game categories.")
def get_categories(search: str = "", platforms: list[Platform] | None = None) -> dict:
    """
    Fetches a list of game categories.

    Args:
        search: A search query to filter categories by name.
        platforms: A list of platforms to filter by.

    Returns:
        A dictionary containing a list of categories.
    """
    client = MiniReviewClient()
    return client.get_categories(search, platforms)


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
    orderBy: OrderBy = OrderBy.LAST_ADDED_REVIEWS,
    platforms: list[Platform] | None = None,
    players: list[str] | None = None,
    network: str | None = None,
    monetization_android: list[str] | None = None,
    monetization_ios: list[str] | None = None,
    screen_orientation: str | None = None,
    category: str | None = None,
    sub_category: str | None = None,
    tags: list[str] | None = None,
    countries_android: list[str] | None = None,
    countries_ios: list[str] | None = None,
    score: dict[str, int] | None = None,
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
    client = MiniReviewClient()
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
    for game in games["results"]:
        game["details"] = client.get_game_details(game["slug"], game["category"])
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
    platforms: list[Platform] | None = None,
    orderBy: OrderBy = OrderBy.MOST_POPULAR,
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
    client = MiniReviewClient()
    games = client.get_similar_games(game_id, page, limit, platforms, orderBy)
    for game in games["results"]:
        game["details"] = client.get_game_details(game["slug"], game["category"])
    return games


if __name__ == "__main__":
    app.run()
