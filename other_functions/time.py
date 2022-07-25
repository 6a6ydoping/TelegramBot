from datetime import datetime


def get_datetime_now():
    delta = datetime.timedelta(hours=6, minutes=0)
    return datetime.datetime.now(datetime.timezone.utc) + delta
