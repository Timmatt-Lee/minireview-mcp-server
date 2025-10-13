from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.tools.load_memory_tool import LoadMemoryTool

async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)

root_agent =  LlmAgent(
    model=Gemini(),
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
        ),
        LoadMemoryTool()
    ],
    after_agent_callback=auto_save_session_to_memory_callback,
)
