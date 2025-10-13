# MiniReview MCP Server

This project exposes the [minireview.io](https://minireview.io/) API as an MCP
server. It's built with the
[fastmcp](https://github.com/jlowin/fastmcp) library, which is a high-level
framework for building MCP servers.

You can interact with the MCP server using any MCP client compatible interface, e.g. Gemini CLI, ADK, etc.

This project also implement the example ADK agent to interact with the MCP server.


## Project Structure

- `minireview_client/`: A Python client for [minireview.io](https://minireview.io/) API.
-   `server.py`: The MCP server wrap with `minireview_client`, built with `fastmcp`.
-   `minireview_agent/`: The ADK agent that connects to the MCP server (`server.py`).

## Getting Started

To get started, you'll need to have Python 3.10+ and pip installed.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Timmatt-Lee/minireview-mcp-server.git
    cd minireview-mcp-server
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage with Gemini CLI

You can interact with the MCP server using Gemini CLI.

Install [Gemini CLI](https://github.com/google/gemini-cli) and launch it in this folder, this MCP server will automatically attach to Gemini CLI.

## Usage with ADK

You can interact with the MCP server using the `adk web` command. This will
start a web-based interface for the agent.

First, you need to set up your environment by creating a `.env` file in the
`minireview_agent` directory. You can find detailed instructions on how to do
this in the
[ADK documentation](https://google.github.io/adk-docs/get-started/quickstart/#set-up-the-model).

Once you have configured your `.env` file, you can start the web interface with
the following command:

```bash
adk web --session_service_uri="sqlite:///session.db"
```



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.