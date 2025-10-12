"""
Enums for the minireview.io API client.
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


class Players(Enum):
    """Represents the player modes for games."""

    SINGLEPLAYER = "singleplayer"
    MULTIPLAYER = "multiplayer"
    PVE = "pve"
    PVP = "pvp"
    REAL_TIME_PVP = "real-time-pvp"
    CO_OP = "co-op"


class Network(Enum):
    """Represents the network requirements for games."""

    ONLINE = "online"
    OFFLINE = "offline"


class Monetization(Enum):
    """Represents the monetization models for games."""

    NO_ADS = "no-ads"
    FREE = "free"
    NO_IAP = "no-iap"
    PAID = "paid"
    TRIAL = "trial"
    PLAY_PASS = "play-pass"


class ScreenOrientation(Enum):
    """Represents the screen orientation for games."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class Category(Enum):
    """Represents the main categories of games."""

    ACTION = "action"
    ADVENTURE = "adventure"
    ARCADE = "arcade"
    AUTO_BATTLER = "auto-battler"
    BATTLE_ROYALE = "battle-royale"
    BOARD = "board"
    CARD = "card"
    CASUAL = "casual"
    CCG = "ccg"
    DECK_BUILDING = "deck-building"
    EDUCATIONAL = "educational"
    FIGHTING = "fighting"
    FLYING = "flying"
    FPS = "fps"
    GACHA = "gacha"
    INCREMENTAL = "incremental"
    MMO = "mmo"
    MMORPG = "mmorpg"
    MOBA = "moba"
    MUSIC = "music"
    PLATFORM = "platform"
    PUZZLE = "puzzle"
    RACING = "racing"
    ROLE_PLAYING = "role-playing"
    RUNNER = "runner"
    RTS = "rts"
    SHOOTER = "shooter"
    SIMULATION = "simulation"
    SPORTS = "sports"
    STRATEGY = "strategy"
    SURVIVAL = "survival"
    TOWER_DEFENSE = "tower-defense"
    TOWER_RUSH = "tower-rush"
    TRIVIA = "trivia"
    WORD = "word"


class SubCategory(Enum):
    """Represents the sub-categories of games."""

    IO = ".io"
    BULLET_HEAVEN = "bullet-heaven"
    BULLET_HELL = "bullet-hell"
    CITY_BUILDING = "city-building"
    DRIFTING = "drifting"
    DUNGEON_CRAWLER = "dungeon-crawler"
    ENDLESS = "endless"
    GOLF = "golf"
    HORROR = "horror"
    MANAGEMENT = "management"
    MATCH_3 = "match-3"
    PHYSICS_BASED = "physics-based"
    POINT_N_CLICK = "point-n-click"
    REVIEWS = "reviews"
    RHYTHM = "rhythm"
    ROGUELIKE = "roguelike"
    SANDBOX = "sandbox"
    STORY_DRIVEN = "story-driven"
    TEXT_BASED = "text-based"


class Tag(Enum):
    """Represents the tags that can be applied to games."""

    TWOD = "2d"
    THREED = "3d"
    ACHIEVEMENTS = "achievements"
    ATMOSPHERIC = "atmospheric"
    AUTO_MODE = "auto-mode"
    AUTO_SHOOTING = "auto-shooting"
    BASE_BUILDING = "base-building"
    CARDS = "cards"
    COMPETITIVE = "competitive"
    CONTROLLER_SUPPORT = "controller-support"
    COSMETICS = "cosmetics"
    CRAFTING = "crafting"
    CROSSPLAY = "crossplay"
    ENERGY_SYSTEM = "energy-system"
    ESPORTS = "esports"
    EXPLORATION = "exploration"
    FRIEND_LIST = "friend-list"
    FUNNY = "funny"
    GUILDS = "guilds"
    HACK_AND_SLASH = "hack-and-slash"
    HARDCORE = "hardcore"
    HIDDEN_OBJECT = "hidden-object"
    IDLE = "idle"
    INDIE = "indie"
    ISOMETRIC = "isometric"
    LEADERBOARDS = "leaderboards"
    JRPG = "jrpg"
    LEVEL_EDITOR = "level-editor"
    LOCAL_MULTIPLAYER = "local-multiplayer"
    LOCAL_WIFI_MULTIPLAYER = "local-wi-fi-multiplayer"
    LOOT = "loot"
    LOOT_BOXES = "loot-boxes"
    MERGE = "merge"
    MINIMALIST = "minimalist"
    METROIDVANIA = "metroidvania"
    NSFW = "nsfw"
    OLDSCHOOL = "oldschool"
    ONLINE_EVENTS = "online-events"
    OPEN_WORLD = "open-world"
    P2W = "p2w"
    PLAY_TO_EARN = "play-to-earn"
    PETS = "pets"
    PHYSICS = "physics"
    PIXEL_ART = "pixel-art"
    PLAYER_ECONOMY = "player-economy"
    PORT = "port"
    PROCEDURAL_GENERATION = "procedural-generation"
    QUESTS = "quests"
    RAIDS = "raids"
    RELAXING = "relaxing"
    SANDBOX = "sandbox"
    STEALTH = "stealth"
    SCI_FI = "sci-fi"
    SEASON_PASS = "season-pass"
    SIDE_SCROLLING = "side-scrolling"
    SUBSCRIPTION = "subscription"
    TOURNAMENTS = "tournaments"
    TURN_BASED = "turn-based"
    VIP_SYSTEM = "vip-system"
    TWIN_STICK = "twin-stick"
    VIRTUAL_JOYSTICK = "virtual-joystick"
    VOICE_CHAT = "voice-chat"
    WAR = "war"
    ZOMBIES = "zombies"


class SideContent(Enum):
    """Represents the types of side content available on the website."""

    REVIEWS = "reviews"
    TOPGAMES = "topgames"
    UPCOMING_GAMES = "upcoming-games"


class Action(Enum):
    """Represents the actions that can be performed on certain endpoints."""

    GET_SIDE_CONTENT = "get-side-content"
    MAIN_PAGE = "main-page"


class Score(Enum):
    """Represents the score categories."""

    GAMEPLAY = "gameplay"
    CONTROLS = "controls"
    GRAPHICS = "graphics"
    MONETIZATION = "monetization"
