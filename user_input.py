"""Collect the stock symbol, chart type, and time series selection."""


def get_stock_symbol():
    """Ask for a nonempty stock symbol and return it in uppercase."""
    while True:
        symbol = input("Enter the stock symbol: ").strip().upper()

        if symbol:
            return symbol

        print("Please enter a stock symbol.")


def get_chart_type():
    """Return the selected chart type: bar or line."""
    while True:
        print("\nChart Types")
        print("1. Bar")
        print("2. Line")

        choice = input("Enter the chart type (1, 2): ").strip()

        if choice == "1":
            return "bar"
        elif choice == "2":
            return "line"

        print("Enter a 1 or 2 for chart type.")


def get_time_series():
    """Return the selected time series."""
    choices = {
        "1": "intraday",
        "2": "daily",
        "3": "weekly",
        "4": "monthly",
    }

    while True:
        print("\nTime Series")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly")

        choice = input("Enter the time series (1, 2, 3, 4): ").strip()

        if choice in choices:
            return choices[choice]

        print("Enter a 1, 2, 3, or 4 for time series.")


def get_user_inputs():
    """Collect the three selections and return them as a dictionary."""
    print("\nStock Data Visualizer")
    print("---------------------")

    return {
        "symbol": get_stock_symbol(),
        "chart_type": get_chart_type(),
        "time_series": get_time_series(),
    }


if __name__ == "__main__":
    selections = get_user_inputs()
    print("\nYour selections:", selections)