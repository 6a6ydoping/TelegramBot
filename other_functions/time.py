import datetime
from datetime import date


def get_datetime_now():
    delta = datetime.timedelta(hours=6, minutes=0)
    d = datetime.datetime.now(datetime.timezone.utc) + delta
    t1 = '%d-%m-%y'
    t2 = '%H:%M:%S'
    return d.strftime(t1), d.strftime(t2)


def is_working_time():
    current_time = get_datetime_now()[1]
    weekday = datetime.datetime.today().weekday()
    start_of_day = '8:00:00'
    end_of_day = '17:30:00'
    if start_of_day <= current_time < end_of_day and 0 <= weekday <= 4:
        return True
    return False

