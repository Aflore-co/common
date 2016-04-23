import pytz
import datetime


def now():
    """
    Returns a timezone-aware datetime representing the current time in UTC.
    """

    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


def bogota_now():
    """
    Return a a timezone-aware datetime representing the current time in Bogotá, Colombia.
    """

    return now().astimezone(pytz.timezone('America/Bogota'))