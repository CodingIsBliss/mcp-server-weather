"""MCP Weather Server – exposes weather lookup tools over streamable-http.

Uses deterministic mock data so the server works without any API keys.
"""

from __future__ import annotations

import hashlib
import math
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

# ---------------------------------------------------------------------------
# Helpers – deterministic "random" weather based on city name + date
# ---------------------------------------------------------------------------

_CONDITIONS = [
    "Sunny", "Partly Cloudy", "Cloudy", "Overcast",
    "Light Rain", "Rain", "Thunderstorm", "Snow",
    "Fog", "Windy", "Clear",
]


def _seed(city: str) -> int:
    """Produce a stable int seed from a city name + today's date."""
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return int(hashlib.md5(f"{city.lower()}:{day}".encode()).hexdigest(), 16)


def _mock_weather(city: str) -> dict:
    s = _seed(city)
    temp_c = -10 + (s % 45)  # -10 … 34 °C
    humidity = 20 + (s >> 4) % 61  # 20 … 80 %
    condition = _CONDITIONS[s % len(_CONDITIONS)]
    wind_kph = round(5 + math.sin(s) * 25, 1)
    return {
        "city": city.title(),
        "temperature_c": temp_c,
        "temperature_f": round(temp_c * 9 / 5 + 32, 1),
        "humidity_pct": humidity,
        "condition": condition,
        "wind_kph": abs(wind_kph),
        "observed_utc": datetime.now(timezone.utc).isoformat(),
    }


def _mock_forecast(city: str, days: int) -> list[dict]:
    forecasts = []
    base = _seed(city)
    for i in range(days):
        s = base + i * 7919  # offset per day
        hi = -5 + (s % 40)
        lo = hi - 3 - (s >> 3) % 8
        condition = _CONDITIONS[s % len(_CONDITIONS)]
        forecasts.append({
            "day": i + 1,
            "high_c": hi,
            "low_c": lo,
            "condition": condition,
        })
    return forecasts


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Get the current weather for a city (mock data, no API key needed)."""
    return _mock_weather(city)


@mcp.tool()
def get_forecast(city: str, days: int = 5) -> dict:
    """Get a multi-day weather forecast for a city.

    Args:
        city: Name of the city.
        days: Number of forecast days (1-10, default 5).
    """
    days = max(1, min(days, 10))
    return {
        "city": city.title(),
        "days": days,
        "forecast": _mock_forecast(city, days),
    }


@mcp.tool()
def compare_weather(cities: list[str]) -> list[dict]:
    """Compare current weather across multiple cities (max 10)."""
    return [_mock_weather(c) for c in cities[:10]]


def main():
    """Entry-point used by the console-script."""
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
