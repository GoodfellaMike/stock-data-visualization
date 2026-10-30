import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

TIME_SERIES_FUNCTIONS = {
    "intraday": "TIME_SERIES_INTRADAY",
    "daily": "TIME_SERIES_DAILY",
    "weekly": "TIME_SERIES_WEEKLY",
    "monthly": "TIME_SERIES_MONTHLY",
}


def get_stock_data(symbol, function):
    if not API_KEY:
        raise ValueError(
            "API key missing. Check your .env file."
        )

    symbol = symbol.strip().upper()
    function = function.strip().lower()

    if not symbol:
        raise ValueError("Stock symbol cannot be empty.")

    if function not in TIME_SERIES_FUNCTIONS:
        raise ValueError("Invalid time-series selection.")

    api_function = TIME_SERIES_FUNCTIONS[function]

    params = {
        "function": api_function,
        "symbol": symbol,
        "apikey": API_KEY,
        "datatype": "json",
    }

    if function == "daily":
        params["outputsize"] = "full"

    if function == "intraday":
        params["interval"] = "60min"
        params["outputsize"] = "full"

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if "Note" in data or "Information" in data:
        message = data.get(
            "Note", data.get("Information")
        )
        raise ValueError(
            f"Alpha Vantage notice: {message}"
        )

    return data


def extract_time_series(data):
    for key in data:
        if "Time Series" in key:
            return data[key]

    raise ValueError(
        "No time-series data found in the API response."
    )


