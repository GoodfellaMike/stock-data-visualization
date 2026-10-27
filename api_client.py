import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

TIME_SERIES_FUNCTIONS = {
    "1": "TIME_SERIES_DAILY",
    "2": "TIME_SERIES_WEEKLY",
    "3": "TIME_SERIES_MONTHLY",
}

def get_stock_data(symbol, function):
    if not API_KEY:
        raise ValueError( "API key missing. Check your .env file.")

    symbol = symbol.strip().upper()

    if not symbol:
        raise ValueError("Stock symbol cannot be empty.")

    if function not in TIME_SERIES_FUNCTIONS.values():
        raise ValueError("Invalid time-series function.")

    params = {
        "function": function,
        "symbol": symbol.strip().upper(),
        "apikey": API_KEY,
        "datatype": "json",
    }

    if function == "TIME_SERIES_DAILY":
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
        raise ValueError(f"Alpha Vantage notice: {message}")

    return data

def extract_time_series(data):
    for key in data:
        if "Time Series" in key:
            return data[key]

    raise ValueError(
        "No time-series data found in the API response."
    )


