"""
This module contains the MiniReviewClient class, which is the main entry point
for interacting with the minireview.io API.
"""

from enum import Enum
from typing import Any, Optional

import requests

from .enums import (
    Action,
    Category,
    CollectionsOrderBy,
    GameRatingsOrderBy,
    Monetization,
    Network,
    OrderBy,
    Platform,
    Players,
    Score,
    ScreenOrientation,
    SideContent,
    SubCategory,
    Tag,
)
from .exceptions import APIError


class MiniReviewClient:
    """A client for the minireview.io API (v2)."""

    BASE_URL = "https://minireview.io/apiv2"

    def __init__(self):
        self._session = requests.Session()
        self._filters_cache: Optional[dict] = None

    def _build_params(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Builds a dictionary of query parameters, filtering out None values and
        handling enums and lists.

        Args:
            params: A dictionary of parameters to process.

        Returns:
            A dictionary of processed query parameters.
        """
        processed_params = {}
        for key, value in params.items():
            if value is None:
                continue

            if isinstance(value, Enum):
                processed_params[key] = value.value
            elif isinstance(value, list):
                # Handle lists of Enums or strings
                processed_params[f"{key}[]"] = [
                    v.value if isinstance(v, Enum) else v for v in value
                ]
            elif isinstance(value, dict):
                for s, v in value.items():
                    processed_params[f"score[{s.value}]"] = v
            elif isinstance(value, bool):
                processed_params[key] = 1 if value else 0
            else:
                processed_params[key] = value

        return processed_params

    def _fetch_api(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        A private method to fetch data from the minireview.io API.

        Args:
            endpoint: The API endpoint to call (e.g., '/games').
            params: A dictionary of query parameters.

        Returns:
            The JSON response from the API.

        Raises:
            APIError: If the API returns an error.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(
                f"An error occurred while fetching data from {url}: {e}"
            ) from e

    def get_filters(self) -> dict:
        """
        Fetches the available filters for the /games endpoint.

        The 'filtros' object in the API response contains a wealth of metadata
        about the available filters. This function retrieves that object and
        caches it for the lifetime of the client instance.

        Returns:
            A dictionary representing the 'filtros' object.
        """
        if self._filters_cache:
            return self._filters_cache

        # We only need one game to get the 'filtros' object
        games_data = self.get_games_list(limit=1)
        if "filtros" in games_data:
            self._filters_cache = games_data["filtros"]
            return self._filters_cache

        return {}

    def get_countries(self) -> dict:
        """
        Fetches the available countries for the /games endpoint.

        Returns:
            A dictionary of countries, with country codes as keys and country names
            as values.
        """
        filters = self.get_filters()
        countries = {}
        for f in filters:
            if f["slug"] == "countries-android":
                for country in f["itens"]:
                    countries[country["slug"]] = country["nome"]
        return countries

    def get_games_list(
        self,
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
        """
        Fetches a list of games with extensive filtering capabilities.
        """
        params = self._build_params(
            {
                "page": page,
                "limit": limit,
                "search": search,
                "orderBy": orderBy,
                "platforms": platforms,
                "players": players,
                "network": network,
                "monetization-android": monetization_android,
                "monetization-ios": monetization_ios,
                "screen-orientation": screen_orientation,
                "category": category,
                "sub-category": sub_category,
                "tags": tags,
                "countries-android": countries_android,
                "countries-ios": countries_ios,
                "score": score,
            }
        )
        return self._fetch_api("/games", params)

    def get_game_details(self, game_slug: str, category: str) -> dict:
        """
        Fetches details for a specific game.
        """
        params = {"getBy": "slug", "category": category}
        return self._fetch_api(f"/games/{game_slug}", params)

    def get_game_ratings(
        self,
        game_id: int,
        page: int = 1,
        limit: int = 50,
        orderBy: GameRatingsOrderBy = GameRatingsOrderBy.NEWEST,
    ) -> dict:
        """
        Fetches ratings for a specific game.
        """
        params = self._build_params(
            {
                "game_id": game_id,
                "page": page,
                "limit": limit,
                "orderBy": orderBy,
            }
        )
        return self._fetch_api("/games-ratings", params)

    def get_similar_games(
        self,
        game_id: int,
        page: int = 1,
        limit: int = 50,
        platforms: Optional[list[Platform]] = None,
        orderBy: OrderBy = OrderBy.MOST_POPULAR,
    ) -> dict:
        """
        Fetches games similar to a specific game.
        """
        params = self._build_params(
            {
                "from_page": "game-page",
                "game_id": game_id,
                "page": page,
                "limit": limit,
                "orderBy": orderBy,
                "platforms": platforms,
            }
        )
        return self._fetch_api("/games-similar", params)

    def get_side_content(
        self, platforms: list[Platform], content: list[SideContent]
    ) -> dict:
        """
        Fetches side content for the website.
        """
        params = self._build_params(
            {
                "acao": Action.GET_SIDE_CONTENT,
                "platforms": platforms,
                "c": content,
            }
        )
        return self._fetch_api("/general/rota_acao", params)

    def get_collections(
        self,
        page: int = 1,
        limit: int = 50,
        search: str = "",
        orderBy: CollectionsOrderBy = CollectionsOrderBy.MOST_POPULAR,
        loadNew: bool = True,
        loadLastUpdated: bool = True,
    ) -> dict:
        """
        Fetches collections of games.
        """
        params = self._build_params(
            {
                "page": page,
                "limit": limit,
                "search": search,
                "orderBy": orderBy,
                "loadNewcollections": loadNew,
                "loadLastUpdatedcollections": loadLastUpdated,
            }
        )
        return self._fetch_api("/collections", params)

    def get_home(
        self,
        page: int = 1,
        platforms: Optional[list[Platform]] = None,
        ids_ignore: Optional[list[int]] = None,
        orderBy: OrderBy = OrderBy.LAST_ADDED_REVIEWS,
    ) -> dict:
        """
        Fetches the home page content.
        """
        params = self._build_params(
            {
                "page": page,
                "orderBy": orderBy,
                "platforms": platforms,
                "ids_ignore": ",".join(map(str, ids_ignore)) if ids_ignore else None,
            }
        )
        return self._fetch_api("/home", params)

    def get_games_of_the_week(
        self,
        page: int = 1,
        limit: int = 50,
        orderBy: OrderBy = OrderBy.WEEK,
        platforms: Optional[list[Platform]] = None,
    ) -> dict:
        """
        Fetches games of the week.
        """
        params = self._build_params(
            {
                "type": "games-of-the-week",
                "page": page,
                "limit": limit,
                "orderBy": orderBy,
                "platforms": platforms,
            }
        )
        return self._fetch_api("/games", params)

    def get_top_user_ratings(
        self,
        page: int = 1,
        limit: int = 50,
        orderBy: OrderBy = OrderBy.THIS_WEEK,
        platforms: Optional[list[Platform]] = None,
    ) -> dict:
        """
        Fetches top user ratings.
        """
        params = self._build_params(
            {
                "page": page,
                "limit": limit,
                "orderBy": orderBy,
                "platforms": platforms,
            }
        )
        return self._fetch_api("/top-user-ratings", params)

    def get_upcoming_games(
        self,
        page: int = 1,
        limit: int = 50,
        orderBy: OrderBy = OrderBy.LAUNCH_DATE,
        platforms: Optional[list[Platform]] = None,
    ) -> dict:
        """
        Fetches upcoming games.
        """
        params = self._build_params(
            {
                "page": page,
                "limit": limit,
                "orderBy": orderBy,
                "platforms": platforms,
            }
        )
        return self._fetch_api("/upcoming-games", params)

    def get_similar_games_main_page(
        self, platforms: Optional[list[Platform]] = None
    ) -> dict:
        """
        Fetches similar games for the main page.
        """
        params = self._build_params(
            {
                "acao": Action.MAIN_PAGE,
                "platforms": platforms,
            }
        )
        return self._fetch_api("/games-similar/rota_acao", params)

    def get_top_games(self, page: int = 1, limit: int = 50, search: str = "") -> dict:
        """
        Fetches top games.
        """
        params = self._build_params(
            {
                "page": page,
                "limit": limit,
                "search": search,
            }
        )
        return self._fetch_api("/top-games", params)

    def get_special_top_games(self, slug: str) -> dict:
        """
        Fetches special top games by slug.
        """
        return self._fetch_api(f"/special-top-games/{slug}")

    def get_categories(
        self, search: str = "", platforms: Optional[list[Platform]] = None
    ) -> dict:
        """
        Fetches a list of categories.
        """
        params = self._build_params(
            {
                "search": search,
                "platforms": platforms,
            }
        )
        return self._fetch_api("/categories", params)