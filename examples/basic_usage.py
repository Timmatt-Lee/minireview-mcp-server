"""
This module contains examples of how to use the MiniReviewClient.
"""

from minireview_client.client import MiniReviewClient
from minireview_client.enums import (
    Category,
    CollectionsOrderBy,
    Monetization,
    Network,
    OrderBy,
    Platform,
    Players,
    Score,
    SideContent,
    Tag,
)
from minireview_client.exceptions import APIError


def main():
    """Main function to run the examples."""
    client = MiniReviewClient()

    print("--- Running MiniReviewClient Examples ---")

    # Example 1: Discover and print all available filters
    print("\n--- 1. Discovering Available Filters ---")
    try:
        client.get_filters()
        print("Successfully fetched filters.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 2: Get available countries
    print("\n--- 2. Fetching Available Countries ---")
    try:
        countries = client.get_countries()
        print(f"Successfully fetched {len(countries)} countries.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 3: Fetch a list of games with complex filters
    print("\n--- 3. Fetching Filtered Games (Complex) ---")
    try:
        client.get_games_list(
            limit=2,
            orderBy=OrderBy.MOST_POPULAR,
            platforms=[Platform.ANDROID],
            players=[Players.SINGLEPLAYER, Players.PVP],
            network=Network.OFFLINE,
            monetization_android=[Monetization.FREE, Monetization.NO_ADS],
            category=Category.STRATEGY,
            tags=[Tag.PIXEL_ART, Tag.TURN_BASED],
            score={Score.GAMEPLAY: 8, Score.GRAPHICS: 7},
        )
        print("Successfully fetched filtered games.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 4: Fetch details for a specific game
    print("\n--- 4. Fetching Game Details ---")
    try:
        # Replace 'vampire-survivors' and 'action' with a valid game slug and category
        game_details = client.get_game_details("vampire-survivors", "action")
        print(
            f"Successfully fetched details for game: {game_details.get('title', 'N/A')}"
        )

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 5: Fetch ratings for a specific game
    print("\n--- 5. Fetching Game Ratings ---")
    try:
        # Replace with a valid game ID
        client.get_game_ratings(game_id=1310, limit=2)
        print("Successfully fetched game ratings.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 6: Fetch similar games
    print("\n--- 6. Fetching Similar Games ---")
    try:
        # Replace with a valid game ID
        client.get_similar_games(game_id=1310, limit=2)
        print("Successfully fetched similar games.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 7: Fetch side content
    print("\n--- 7. Fetching Side Content ---")
    try:
        client.get_side_content(
            platforms=[Platform.ANDROID, Platform.IOS],
            content=[SideContent.TOPGAMES, SideContent.UPCOMING_GAMES],
        )
        print("Successfully fetched side content.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 8: Fetch game collections
    print("\n--- 8. Fetching Game Collections ---")
    try:
        client.get_collections(limit=2, orderBy=CollectionsOrderBy.NEWEST)
        print("Successfully fetched game collections.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 9: Fetch home page content
    print("\n--- 9. Fetching Home Page Content ---")
    try:
        client.get_home(platforms=[Platform.ANDROID])
        print("Successfully fetched home page content.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 10: Fetch Games of the Week
    print("\n--- 10. Fetching Games of the Week ---")
    try:
        client.get_games_of_the_week(limit=2, platforms=[Platform.IOS])
        print("Successfully fetched Games of the Week.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 11: Fetch Top User Ratings
    print("\n--- 11. Fetching Top User Ratings ---")
    try:
        client.get_top_user_ratings(limit=2)
        print("Successfully fetched top user ratings.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 12: Fetch Upcoming Games
    print("\n--- 12. Fetching Upcoming Games ---")
    try:
        client.get_upcoming_games(limit=2, orderBy=OrderBy.LAUNCH_DATE)
        print("Successfully fetched upcoming games.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 13: Fetch Similar Games for Main Page
    print("\n--- 13. Fetching Similar Games (Main Page) ---")
    try:
        client.get_similar_games_main_page(platforms=[Platform.ANDROID])
        print("Successfully fetched similar games for the main page.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 14: Fetch Top Games
    print("\n--- 14. Fetching Top Games ---")
    try:
        client.get_top_games(limit=2, search="dungeon")
        print("Successfully fetched top games.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 15: Fetch Special Top Games
    print("\n--- 15. Fetching Special Top Games ---")
    try:
        # Replace with a valid slug like 'best-mobile-games-2023'
        client.get_special_top_games(slug="best-mobile-games-2023")
        print("Successfully fetched special top games.")

    except APIError as e:
        print(f"An error occurred: {e}")

    # Example 16: Fetch Categories
    print("\n--- 16. Fetching Categories ---")
    try:
        categories = client.get_categories(platforms=[Platform.ANDROID, Platform.IOS])
        print(f"Successfully fetched {len(categories)} categories.")

    except APIError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
