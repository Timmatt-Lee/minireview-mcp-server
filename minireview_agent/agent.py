from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.genai import types
from mcp import StdioServerParameters

root_agent =  LlmAgent(
    model=Gemini(model='gemini-2.5-pro', retry_options=types.HttpRetryOptions(initial_delay=1, attempts=2),),
    name='MiniReview',
    instruction='You are a mobile game expert. You can help users find games, get details about them, and much more. You are using the MiniReview API to get the information.',
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='python',
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
