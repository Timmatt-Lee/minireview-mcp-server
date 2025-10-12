# MiniReview MCP Server

This project provides a Model Context Protocol (MCP) server for the
[minireview.io API](https://minireview.io/).

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.
