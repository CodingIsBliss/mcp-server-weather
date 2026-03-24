# MCP Server – Weather 🌤️

A **Model Context Protocol (MCP)** server that provides weather lookup tools
via the **streamable-http** transport.

Uses deterministic mock data (seeded by city name + date) so it runs out of
the box with **zero API keys**.

Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk).

## Quick Start

```bash
# Install
pip install -e .

# Run (streamable-http on port 8000)
mcp-server-weather
```

The server listens on `http://0.0.0.0:8000/mcp` by default.

## Available Tools

| Tool                | Description                                        |
|---------------------|----------------------------------------------------|
| `get_current_weather` | Current temperature, humidity, condition for a city |
| `get_forecast`        | Multi-day forecast (1-10 days)                    |
| `compare_weather`     | Side-by-side weather for multiple cities           |

## Environment Variable Overrides

| Variable        | Default              |
|-----------------|----------------------|
| `MCP_TRANSPORT` | `streamable-http`    |
| `MCP_HOST`      | `0.0.0.0`           |
| `MCP_PORT`      | `8000`              |

## License

MIT
