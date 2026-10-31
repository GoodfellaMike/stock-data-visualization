
import requests

from user_input import get_user_inputs
from api_client import get_stock_data, extract_time_series
from validation import validate_date_range
from visualization import generate_chart


def get_dates():
    """Ask the user for a valid date range."""
    while True:
        start_date = input(
            "\nEnter beginning date (YYYY-MM-DD): "
        ).strip()

        end_date = input(
            "Enter ending date (YYYY-MM-DD): "
        ).strip()

        try:
            return validate_date_range(start_date, end_date)

        except ValueError as error:
            print(f"\nInvalid date range: {error}")
            print("Please try again.")


def main():
    print("================================")
    print("   Stock Data Visualization")
    print("   INFOTC 4320 - Project 3")
    print("================================")

    while True:
        try:
            # Get user selections
            selections = get_user_inputs()

            symbol = selections["symbol"]
            chart_type = selections["chart_type"]
            time_series = selections["time_series"]

            # Get validated date range
            start_date, end_date = get_dates()

            # Retrieve stock information
            print("\nRetrieving stock data...")

            api_response = get_stock_data(
                symbol, time_series
            )

            stock_data = extract_time_series(
                api_response
            )

            # Generate and display chart
            print("Generating your chart...")

            generate_chart(
                stock_data,
                symbol,
                chart_type,
                start_date,
                end_date
            )

            print("\nChart opened successfully!")

        except (ValueError, requests.RequestException) as error:
            print(f"\nError: {error}")

        except Exception as error:
            print(f"\nAn unexpected error occurred: {error}")

        # Allow multiple searches
        while True:
            again = input(
                "\nWould you like to search another stock? (y/n): "
            ).strip().lower()

            if again in ("y", "yes", "n", "no"):
                break

            print("Please enter y or n.")

        if again in ("n", "no"):
            print("\nThank you for using Stock Data Visualization!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nApplication closed.")
