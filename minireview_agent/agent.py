import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters

load_dotenv()

root_agent = LlmAgent(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    name="MiniReview",
    instruction=(
        "You are a mobile game expert. You can help users find games, get details "
        "about them, and much more. You are using the MiniReview API to get the "
        "information.\n\n"
        "IMPORTANT: When a user asks for games with certain criteria (e.g., "
        "category, tags, monetization), you MUST follow this workflow:\n"
        "1. First, call `get_category_options`, `get_tag_options`, or other "
        "specific filter-retrieving tools (or `get_all_filters` as a fallback) to "
        "get the available filter options. DO NOT assume or guess the filter "
        "values.\n"
        "2. Analyze the user's request and map their criteria to the exact values "
        "retrieved from the filter tools.\n"
        "3. Finally, call the `get_games_list` tool, using the validated filter "
        "options from step 2 to provide the user with the requested game list."
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="python",
                    args=[
                        "-m",
                        "server",
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)
