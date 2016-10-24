"""
Utility functions should go in here
"""
from datetime import timedelta


def emit_week(day):
    """
    Given a day calculate from the Sunday - to the past Monday
    :param day: must be datetime object
    :return:
    """
    day_of_week = day.weekday()

    # tosunday
    to_beginning_of_week = timedelta(days=day_of_week)
    beginning_of_week = day - to_beginning_of_week - timedelta(days=1)

    to_end_of_week = timedelta(days=-6)
    end_of_week = beginning_of_week + to_end_of_week

    return (end_of_week, beginning_of_week)