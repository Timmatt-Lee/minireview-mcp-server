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

## Installation

To install the client and server, run the following command:

```bash
pip install .[server]
```

## Running the server

To run the MCP server, run one of the following commands:

```bash
python server.py
```

Or:

```bash
fastmcp run server.py:app
```

## Usage

Once the server is running, you can interact with it using an MCP client. The
server exposes the following tools:

- `get_games_list`: Fetches a list of games with extensive filtering
  capabilities.
- `get_game_details`: Fetches details for a specific game.
- `get_game_ratings`: Fetches ratings for a specific game.
- `get_similar_games`: Fetches games similar to a specific game.
- `get_collections`: Fetches collections of games.
- `get_categories`: Fetches a list of categories.

For example, to get a list of games, you can use the following command:

```bash
fastmcp call get_games_list
```

## Development

To set up the development environment, run the following command:

```bash
pip install -e .[server,dev]
```

To run the tests, run the following command:

```bash
pytest
```

### Running the server in development mode

To run the server in development mode with the MCP Inspector, run the following command:

```bash
fastmcp dev server.py:app
```

This will start the server and open the MCP Inspector in your web browser. The
inspector allows you to see the available tools and to call them with different
parameters.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.
