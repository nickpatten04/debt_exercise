import datetime


def try_cast_to_datetime(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    except Exception:
        return value
