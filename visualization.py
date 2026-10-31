

from datetime import datetime, date

import pandas as pd
import plotly.graph_objects as go


def generate_chart(data, symbol, chart_type, start_date, end_date):
    """
    Generate a stock chart from Alpha Vantage API data.

    Parameters:
        data: Raw API response or extracted time-series dictionary
        symbol: Stock ticker symbol (example: AAPL)
        chart_type: "line" or "bar"
        start_date: Beginning date in YYYY-MM-DD format
        end_date: Ending date in YYYY-MM-DD format
    """

    if chart_type not in ("line", "bar"):
        raise ValueError("Chart type must be 'line' or 'bar'.")

    # Support either the full API response or extracted time-series data
    if isinstance(data, dict):
        for key, value in data.items():
            if "Time Series" in key and isinstance(value, dict):
                data = value
                break

    if not isinstance(data, dict) or not data:
        raise ValueError("No stock data available to display.")

    # Convert dates into date objects
    def parse_date(value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return datetime.strptime(value, "%Y-%m-%d").date()

    start = parse_date(start_date)
    end = parse_date(end_date)

    if start > end:
        raise ValueError("End date cannot be before start date.")

    # Extract closing prices from Alpha Vantage data
    records = []

    for timestamp, values in data.items():
        try:
            stock_date = datetime.strptime(
                timestamp[:10], "%Y-%m-%d"
            ).date()

            if start <= stock_date <= end:
                closing_price = float(values["4. close"])

                records.append({
                    "Date": timestamp,
                    "Close": closing_price
                })

        except (ValueError, TypeError, KeyError):
            continue

    if not records:
        raise ValueError(
            "No stock data found for the selected date range."
        )

    # Create and sort the DataFrame
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    # Create chart based on user selection
    fig = go.Figure()

    if chart_type == "line":
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["Close"],
                mode="lines",
                name="Closing Price"
            )
        )

    elif chart_type == "bar":
        fig.add_trace(
            go.Bar(
                x=df["Date"],
                y=df["Close"],
                name="Closing Price"
            )
        )

    # Chart formatting
    fig.update_layout(
        title=f"{symbol.upper()} Stock Price",
        xaxis_title="Date",
        yaxis_title="Closing Price (USD)",
        template="plotly_white",
        hovermode="x unified"
    )

    # Open chart in the default browser
    fig.show(renderer="browser")

    return fig
