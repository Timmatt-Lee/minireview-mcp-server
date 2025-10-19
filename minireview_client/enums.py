"""
Enums for fixed-value parameters in the minireview.io API client.
"""

from enum import Enum


class GamesListOrderBy(Enum):
    """Represents the available sorting options for game lists."""

    LAST_ADDED_REVIEWS = "last-added-reviews"
    LAST_UPDATED_GAMES = "last-updated-games"
    NEW_ON_MINIREVIEW = "new-on-minireview"
    RELEASE_DATE = "release-date"
    HIGHEST_USER_RATINGS = "highest-user-ratings"
    HIGHEST_SCORE = "highest-score"
    HIGHEST_GOOGLE_PLAY_SCORE = "highest-google-play-score"
    HIGHEST_APP_STORE_SCORE = "highest-appStore-score"


class GameRatingsOrderBy(Enum):
    """Represents the available sorting options for game ratings."""

    NEWEST = "newest"
    OLDEST = "oldest"
    MOST_RELEVANT = "most-relevant"


class Platform(Enum):
    """Represents the available platforms."""

    ANDROID = "android"
    IOS = "ios"


class GameRatingType(Enum):
    """Represents the available game rating types."""

    ALL = "all"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class TopUserRatingsOrderBy(Enum):
    """Represents the available sorting options for top user ratings."""

    THIS_WEEK = "this-week"
    THIS_DATE = "this-month"
    ALL_TIME = "all-time"


class Monetization(Enum):
    """Represents the available monetization types."""

    FREE = "free"
    PAID = "paid"


class Players(Enum):
    """Represents the available player types."""

    SINGLE_PLAYER = "singleplayer"
    MULTI_PLAYER = "multiplayer"


class ScreenOrientation(Enum):
    """Represents the available screen orientations."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
