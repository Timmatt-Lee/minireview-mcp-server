from typing import Optional

from fastmcp import FastMCP
from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    Category,
    CollectionsOrderBy,
    GameRatingsOrderBy,
    Monetization,
    Network,
    OrderBy,
    Platform,
    Players,
    ScreenOrientation,
    Score,
    SubCategory,
    Tag,
)

app = FastMCP()


@app.tool
def get_games_list(
    page: int = 1,
    limit: int = 50,
    search: str = "",
    orderBy: OrderBy = OrderBy.LAST_ADDED_REVIEWS,
    platforms: Optional[list[Platform]] = None,
    players: Optional[list[Players]] = None,
    network: Optional[Network] = None,
    monetization_android: Optional[list[Monetization]] = None,
    monetization_ios: Optional[list[Monetization]] = None,
    screen_orientation: Optional[ScreenOrientation] = None,
    category: Optional[Category] = None,
    sub_category: Optional[SubCategory] = None,
    tags: Optional[list[Tag]] = None,
    countries_android: Optional[list[str]] = None,
    countries_ios: Optional[list[str]] = None,
    score: Optional[dict[Score, int]] = None,
) -> dict:
    """Fetches a list of games with extensive filtering capabilities."""
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


@app.tool
def get_game_details(game_slug: str, category: str) -> dict:
    """Fetches details for a specific game."""
    client = MiniReviewClient()
    return client.get_game_details(game_slug, category)


@app.tool
def get_game_ratings(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    orderBy: GameRatingsOrderBy = GameRatingsOrderBy.NEWEST,
) -> dict:
    """Fetches ratings for a specific game."""
    client = MiniReviewClient()
    return client.get_game_ratings(game_id, page, limit, orderBy)


@app.tool
def get_similar_games(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    platforms: Optional[list[Platform]] = None,
    orderBy: OrderBy = OrderBy.MOST_POPULAR,
) -> dict:
    """Fetches games similar to a specific game."""
    client = MiniReviewClient()
    return client.get_similar_games(game_id, page, limit, platforms, orderBy)


@app.tool
def get_collections(
    page: int = 1,
    limit: int = 50,
    search: str = "",
    orderBy: CollectionsOrderBy = CollectionsOrderBy.MOST_POPULAR,
    loadNew: bool = True,
    loadLastUpdated: bool = True,
) -> dict:
    """Fetches collections of games."""
    client = MiniReviewClient()
    return client.get_collections(page, limit, search, orderBy, loadNew, loadLastUpdated)


@app.tool
def get_categories(search: str = "", platforms: Optional[list[Platform]] = None) -> dict:
    """Fetches a list of categories."""
    client = MiniReviewClient()
    return client.get_categories(search, platforms)


@app.tool
def get_games_list_with_details(
    page: int = 1,
    limit: int = 50,
    search: str = "",
    orderBy: OrderBy = OrderBy.LAST_ADDED_REVIEWS,
    platforms: Optional[list[Platform]] = None,
    players: Optional[list[Players]] = None,
    network: Optional[Network] = None,
    monetization_android: Optional[list[Monetization]] = None,
    monetization_ios: Optional[list[Monetization]] = None,
    screen_orientation: Optional[ScreenOrientation] = None,
    category: Optional[Category] = None,
    sub_category: Optional[SubCategory] = None,
    tags: Optional[list[Tag]] = None,
    countries_android: Optional[list[str]] = None,
    countries_ios: Optional[list[str]] = None,
    score: Optional[dict[Score, int]] = None,
) -> dict:
    """Fetches a list of games with extensive filtering capabilities and then fetches the details for each game."""
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


@app.tool
def get_similar_games_with_details(
    game_id: int,
    page: int = 1,
    limit: int = 50,
    platforms: Optional[list[Platform]] = None,
    orderBy: OrderBy = OrderBy.MOST_POPULAR,
) -> dict:
    """Fetches games similar to a specific game and then fetches the details for each game."""
    client = MiniReviewClient()
    games = client.get_similar_games(game_id, page, limit, platforms, orderBy)
    for game in games["results"]:
        game["details"] = client.get_game_details(game["slug"], game["category"])
    return games


if __name__ == "__main__":
    app.run()
