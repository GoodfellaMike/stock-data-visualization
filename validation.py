from datetime import date, datetime


def validate_date_range(start_date, end_date, today=None):

    Raises ValueError with a useful message when either date is invalid,
    a date is in the future, or the start date is after the end date.
    The optional today argument makes the function easier to test.
