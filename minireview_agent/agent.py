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
        "information."
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
