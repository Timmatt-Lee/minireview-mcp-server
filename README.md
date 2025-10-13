# MiniReview MCP Server

## Which MCP SDK is used?

This project uses the [fastmcp](https://github.com/jlowin/fastmcp) library, which is a
high-level framework for building MCP servers. While the official
[Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
provides the low-level building blocks for MCP, `fastmcp` provides a more
user-friendly, "batteries-included" experience for building servers.

For this particular task, where the goal was to quickly create an MCP server
from an existing API client, `fastmcp` was the more appropriate tool. It allowed
me to define the tools with simple decorators and it handled a lot of the
boilerplate code for me.

## Features

- Exposes the minireview.io API as an MCP server.
- Provides tools for fetching games, ratings, collections, and categories.
- Built with the [fastmcp](https://github.com/modelcontextprotocol/fastmcp)
  library.

## Prerequisites

If you wanna use MiniReview MCP Server in [Gemini CLI](https://github.com/google/gemini-cli), install [Gemini CLI](https://github.com/google/gemini-cli) first

## Usage with ADK

You can also interact with the MCP server using the `adk web` command. This will start a web-based interface for the agent.

First, you need to set up your environment by creating a `.env` file in the `agent` directory.
You can find detailed instructions on how to do this in the [ADK documentation](https://google.github.io/adk-docs/get-started/quickstart/#set-up-the-model).

Your `agent/.env` file should look like this:

```
API_KEY="YOUR_API_KEY"
```

Once you have configured your `.env` file, you can start the web interface with the following command:

```bash
adk web
```

## Usage with Gemini CLI

To use the tools from the Gemini CLI, follow these steps:

```bash
git clone https://github.com/Timmatt-Lee/minireview-mcp-server.git
cd minireview-mcp-server
pip install -r requirements.txt
gemini
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.
