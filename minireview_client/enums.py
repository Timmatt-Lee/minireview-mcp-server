"""
Enums for fixed-value parameters in the minireview.io API client.
"""

from enum import Enum


class OrderBy(Enum):
    """Represents the available sorting options for game lists."""

    LAST_ADDED_REVIEWS = "last-added-reviews"
    NEWEST = "newest"
    MOST_POPULAR = "most-popular"
    THIS_WEEK = "this-week"
    LAUNCH_DATE = "launch-date"
    WEEK = "week"


class CollectionsOrderBy(Enum):
    """Represents the available sorting options for collections."""

    MOST_POPULAR = "most-popular"
    NEWEST = "newest"


class GameRatingsOrderBy(Enum):
    """Represents the available sorting options for game ratings."""

    NEWEST = "newest"
    MOST_POPULAR = "most-popular"


class Platform(Enum):
    """Represents the available platforms."""

    ANDROID = "android"
    IOS = "ios"
