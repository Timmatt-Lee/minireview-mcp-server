"""
This module contains the MiniReviewClient class, which is the main entry point
for interacting with the minireview.io API.
"""

from enum import Enum
from typing import Any

import requests

from .enums import (
    CollectionsOrderBy,
    GameRatingsOrderBy,
    GameRatingType,
    GamesListOrderBy,
    Monetization,
    Platform,
    Players,
    ScreenOrientation,
    TopUserRatingsOrderBy,
)
from .exceptions import APIError


class MiniReviewClient:
    """A client for the minireview.io API (v2)."""

    BASE_URL = "https://minireview.io/apiv2"

    def __init__(self):
        self._session = requests.Session()
        self._filters_cache: dict | None = None
        self._parsed_filters: dict[str, set[str]] | None = None

    def _init_validator(self):
        """
        Initializes a cache of parsed filters for efficient validation.
        This method parses the raw filter data from the API into a
        structure that's quick to check against.
        """
        if self._parsed_filters is not None:
            return

        raw_filters_list = self.get_filters()
        if not raw_filters_list:
            self._parsed_filters = {}
            return

        self._parsed_filters = {
            f["slug"]: {item["slug"] for item in f["itens"]} for f in raw_filters_list
        }

    def _validate_score_param(self, score_value: dict[str, Any]):
        """Validates the 'score' parameter."""
        if not isinstance(score_value, dict):
            raise ValueError("Score parameter must be a dictionary.")

        allowed_keys = self._parsed_filters.get("score", set())
        for s_key, s_value in score_value.items():
            if s_key not in allowed_keys:
                raise ValueError(f"Invalid score key: '{s_key}'")
            if not isinstance(s_value, int) or not (0 <= s_value <= 10):
                raise ValueError(
                    f"Invalid score value for '{s_key}': {s_value}. "
                    "Must be an integer from 0 to 10."
                )

    def _validate_filter_param(self, key: str, value: Any):
        """Validates a generic filter parameter against the API's allowed values."""
        if value is None:
            return
        allowed_values = self._parsed_filters[key]
        values_to_check = value if isinstance(value, list) else [value]

        for v in values_to_check:
            actual_value = v.value if isinstance(v, Enum) else v
            if actual_value not in allowed_values:
                raise ValueError(
                    f"Invalid value for filter '{key}': '{v}'. "
                    "Check get_filters() for options."
                )

    def _validate_params(self, params: dict[str, Any]):
        """
        Validates filter parameters against the allowed values from the API.
        Raises a ValueError for any invalid filter values.
        """
        self._init_validator()
        assert self._parsed_filters is not None

        for key, value in params.items():
            if key == "score":
                self._validate_score_param(value)
            elif key in self._parsed_filters:
                self._validate_filter_param(key, value)

    def _build_params(
        self, params: dict[str, Any], is_validate: bool = False
    ) -> dict[str, Any]:
        """
        Builds a dictionary of query parameters, filtering out None values,
        handling lists, and optionally validating filter values.

        Args:
            params: A dictionary of parameters to process.
            is_validate: If True, validate filter values against the API.

        Returns:
            A dictionary of processed query parameters.
        """
        if is_validate:
            self._validate_params(params)

        processed_params = {}
        for key, value in params.items():
            if value is None or value in ([], {}, ""):
                continue

            if isinstance(value, Enum):
                processed_params[key] = value.value
            elif isinstance(value, list):
                # platforms is the only list that uses indexed keys
                if key == "platforms":
                    for i, v in enumerate(value):
                        processed_params[f"{key}[{i}]"] = (
                            v.value if isinstance(v, Enum) else v
                        )
                # All other lists are comma-separated
                else:
                    processed_params[key] = ",".join(
                        [str(v.value if isinstance(v, Enum) else v) for v in value]
                    )
            elif isinstance(value, dict):
                # Custom handling for "score"
                if key == "score":
                    processed_params[key] = ",".join(
                        [f"{s}-{v}" for s, v in value.items()]
                    )
                else:
                    for s, v in value.items():
                        processed_params[f"{key}[{s}]"] = v
            elif isinstance(value, bool):
                processed_params[key] = 1 if value else 0
            else:
                processed_params[key] = value

        return processed_params

    def _fetch_api(self, endpoint: str, params: dict | None = None) -> dict:
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
        # We call _build_params directly to avoid a validation circular dependency
        params = self._build_params({"limit": 1})
        games_data = self._fetch_api("/games", params)

        if "filtros" in games_data:
            self._filters_cache = games_data["filtros"]
            return self._filters_cache

        return {}

    def _get_filter_options(self, filter_slug: str) -> dict:
        """
        A generic helper to fetch options for a given filter slug.
        """
        filters = self.get_filters()
        for f in filters:
            if f["slug"] == filter_slug:
                return {item["slug"]: item["nome"] for item in f["itens"]}
        return {}

    def get_players(self) -> dict:
        return self._get_filter_options("players")

    def get_network_options(self) -> dict:
        return self._get_filter_options("network")

    def get_monetization_android(self) -> dict:
        return self._get_filter_options("monetization-android")

    def get_monetization_ios(self) -> dict:
        return self._get_filter_options("monetization-ios")

    def get_screen_orientation_options(self) -> dict:
        return self._get_filter_options("screen-orientation")

    def get_category_options(self) -> dict:
        return self._get_filter_options("category")

    def get_sub_category_options(self) -> dict:
        return self._get_filter_options("sub-category")

    def get_tags(self) -> dict:
        return self._get_filter_options("tags")

    def get_countries_android(self) -> dict:
        return self._get_filter_options("countries-android")

    def get_countries_ios(self) -> dict:
        return self._get_filter_options("countries-ios")

    def get_score_options(self) -> dict:
        return self._get_filter_options("score")

    def get_games_list(
        self,
        page: int = 1,
        limit: int = 50,
        search: str = "",
        orderBy: GamesListOrderBy = GamesListOrderBy.LAST_ADDED_REVIEWS,
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
        Fetches a list of games with extensive filtering capabilities.
        """
        params = {
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
        return self._fetch_api("/games", self._build_params(params, is_validate=True))

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
        type: GameRatingType = GameRatingType.ALL,
        orderBy: GameRatingsOrderBy = GameRatingsOrderBy.NEWEST,
    ) -> dict:
        """
        Fetches ratings for a specific game.
        """
        params = {
            "game_id": game_id,
            "page": page,
            "type": type,
            "limit": limit,
            "orderBy": orderBy,
        }
        return self._fetch_api(
            "/games-ratings", self._build_params(params, is_validate=True)
        )

    def get_similar_games(
        self,
        game_id: int,
        page: int = 1,
        limit: int = 50,
        platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
        monetization: Monetization | None = None,
        players: Players | None = None,
        screen_orientation: ScreenOrientation | None = None,
    ) -> dict:
        """
        Fetches games similar to a specific game.
        """
        params = {
            "game_id": game_id,
            "page": page,
            "limit": limit,
            "platforms": platforms,
            "monetization": monetization,
            "players": players,
            "screen-orientation": screen_orientation,
        }
        return self._fetch_api(
            "/games-similar", self._build_params(params, is_validate=True)
        )

    def get_collections(
        self,
        page: int = 1,
        limit: int = 50,
        search: str = "",
        orderBy: CollectionsOrderBy = CollectionsOrderBy.MOST_POPULAR,
        is_load_new: bool = True,
        is_load_last_updated: bool = True,
    ) -> dict:
        """
        Fetches collections of games.
        """
        params = {
            "page": page,
            "limit": limit,
            "search": search,
            "orderBy": orderBy,
            "loadNewcollections": is_load_new,
            "loadLastUpdatedcollections": is_load_last_updated,
        }
        return self._fetch_api(
            "/collections", self._build_params(params, is_validate=True)
        )

    def get_home(
        self,
        page: int = 1,
        platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
        ids_ignore: list[int] = [],
        orderBy: GamesListOrderBy = GamesListOrderBy.LAST_ADDED_REVIEWS,
    ) -> dict:
        """
        Fetches the home page content.
        """
        params = {
            "page": page,
            "orderBy": orderBy,
            "platforms": platforms,
            "ids_ignore": ",".join(map(str, ids_ignore)) if ids_ignore else None,
        }
        return self._fetch_api("/home", self._build_params(params, is_validate=True))

    def get_games_of_the_week(
        self,
        page: int = 1,
        limit: int = 50,
        orderBy: GamesListOrderBy = GamesListOrderBy.LAST_ADDED_REVIEWS,
        platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    ) -> dict:
        """
        Fetches games of the week.
        """
        params = {
            "type": "games-of-the-week",
            "page": page,
            "limit": limit,
            "orderBy": orderBy,
            "platforms": platforms,
        }
        return self._fetch_api("/games", self._build_params(params, is_validate=True))

    def get_top_user_ratings(
        self,
        page: int = 1,
        limit: int = 50,
        orderBy: TopUserRatingsOrderBy = TopUserRatingsOrderBy.THIS_WEEK,
        platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    ) -> dict:
        """
        Fetches top user ratings.
        """
        params = {
            "page": page,
            "limit": limit,
            "orderBy": orderBy,
            "platforms": platforms,
        }
        return self._fetch_api(
            "/top-user-ratings", self._build_params(params, is_validate=True)
        )

    def get_upcoming_games(
        self,
        page: int = 1,
        limit: int = 50,
        orderBy: GamesListOrderBy = GamesListOrderBy.RELEASE_DATE,
        platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    ) -> dict:
        """
        Fetches upcoming games.
        """
        params = {
            "page": page,
            "limit": limit,
            "orderBy": orderBy,
            "platforms": platforms,
        }
        return self._fetch_api(
            "/upcoming-games", self._build_params(params, is_validate=True)
        )

    def get_top_games(self, page: int = 1, limit: int = 50, search: str = "") -> dict:
        """
        Fetches top games.
        """
        params = self._build_params({"page": page, "limit": limit, "search": search})
        return self._fetch_api("/top-games", params)

    def get_special_top_games(self, slug: str) -> dict:
        """
        Fetches special top games by slug.
        """
        return self._fetch_api(f"/special-top-games/{slug}")

    def get_categories(
        self,
        search: str = "",
        platforms: list[Platform] = [Platform.ANDROID, Platform.IOS],
    ) -> dict:
        """
        Fetches a list of categories.
        """
        params = {"search": search, "platforms": platforms}
        return self._fetch_api(
            "/categories", self._build_params(params, is_validate=True)
        )
