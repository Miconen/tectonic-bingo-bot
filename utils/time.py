import time
from enum import Enum

class TimestampType(Enum):
    TIME_SHORT = 't'
    TIME_LONG = 'T'
    DATE_SHORT = 'd'
    DATE_LONG = 'D'
    DATE_TIME_SHORT = 'f'
    DATE_TIME_LONG = 'F'
    RELATIVE = 'R'

def get_time():
    return int(time.time())

def get_relative_time(type: TimestampType, time: float | None = None):
    if time is None:
        time = get_time()
    else:
        time = int(time)

    return f"<t:{time}:{type.value}>"
