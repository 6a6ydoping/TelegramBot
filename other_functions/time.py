import datetime
from datetime import date


def get_datetime_now():
    delta = datetime.timedelta(hours=6, minutes=0)
    d = datetime.datetime.now(datetime.timezone.utc) + delta
    t1 = '%d-%m-%y'
    t2 = '%H:%M:%S'
    return d.strftime(t1), d.strftime(t2)
