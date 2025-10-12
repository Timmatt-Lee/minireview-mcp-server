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

Before you can use this project, you need to install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use the tools from the Gemini CLI, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Timmatt-Lee/minireview-mcp-server.git
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd minireview-mcp-server
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gemini CLI:**

    ```bash
    /opt/homebrew/bin/gemini
    ```

5.  **Check for the available tools:**

    Once you are in the Gemini CLI, you can type `/mcp` to see the available
    tools.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.
