from datetime import datetime, timedelta
from typing import Any
import functools

import homebrain
import os


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None
        functools.update_wrapper(self, cls)

    def __call__(self, *args, **kwds) -> Any:
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance

    def reset_singleton(self):
        """
        Detaches the instance from the singleton, causing the creation of
        a new object when __call__'d.
        Useful in testing.
        """
        self.instance = None


def get_cwd():
    # TODO: Refactor to get_main_directory or something similar
    return os.path.dirname(homebrain.__file__)


def modulo_timedelta(dt: datetime, td: timedelta) -> datetime:
    """
    Takes a datetime to perform modulo on and a timedelta.
    :returns: dt % td
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return timedelta(seconds=((dt - today).total_seconds() % td.total_seconds()))


def floor_datetime(dt: datetime, td: timedelta) -> datetime:
    """
    Floors a datetime with interval zone td
    :returns: dt - dt % td
    """
    return dt - modulo_timedelta(dt, td)


def ceil_datetime(dt: datetime, td: timedelta) -> datetime:
    return floor_datetime(dt, td) + td
