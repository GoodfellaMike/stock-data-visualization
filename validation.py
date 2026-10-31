
from datetime import date, datetime


def validate_date_range(start_date, end_date, today=None):
    """
    Raises ValueError when either date is invalid,
    a date is in the future, or the start date is
    after the end date.
    """
    if today is None:
        today = date.today()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("Dates must be in YYYY-MM-DD format.")

    if start > today or end > today:
        raise ValueError("Dates cannot be in the future.")

    if start > end:
        raise ValueError("End date cannot be before start date.")

    return start, end
