from datetime import datetime

import pytz
from pytz import timezone

UTC = "UTC"


def datetime_timezone(tz=UTC):
    """
    This method returns utcnow with appropriate timezone, or normalized
    to the correct timezone if provided.
    """
    utc_datetime_naive = datetime.utcnow()
    # return a localized datetime to utc
    utc_localized_datetime = localize(utc_datetime_naive, UTC)
    # normalize the datetime to given timezone
    normalized_datetime = normalize(utc_localized_datetime, tz)
    return normalized_datetime


def localize(dt, tz):
    """
    Given a naive datetime object this method will return a localized
    datetime object
    """
    tz = timezone(tz)
    return tz.localize(dt)


def normalize(dt, tz):
    """
    Given a object with a timezone return a datetime object
    normalized to the proper timezone.

    This means take the give datetime and return the datetime shifted
    to match the specificed timezone.
    """
    tz = timezone(tz)
    dt = tz.normalize(dt)
    return dt


def is_datetime_naive(dt):
    """
    Return true if the datetime is naive else returns false
    """
    if dt is None:
        return True

    if dt.tzinfo is None:
        return True
    else:
        return False


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all
    functionality of the Delorean.
    """
    _VALID_SHIFTS = ('day', 'week', 'month', 'year', 'monday', 'tuesday',
                     'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    def __init__(self, datetime=None, timezone=None):
        # maybe set timezone on the way in here. if here set it if not
        # use UTC
        self._tz = timezone
        self._dt = datetime

        if is_datetime_naive(datetime):
            pass
        else:
            # raise a value error since you are passing a localized
            # datetime
            raise ValueError

        if timezone is None and datetime is None:
            self._tz = UTC
            self._dt = datetime_timezone()
        elif timezone is not None and datetime is None:
            # create utctime then normalize to tz
            self._tz = timezone
            self._dt = datetime_timezone(tz=timezone)
        elif timezone is None and datetime is not None:
            raise ValueError
        else:
            # passed in naive datetime and timezone
            # that correspond accordingly
            self._tz = timezone
            self._dt = localize(datetime, timezone)

    def __repr__(self):
        return '<Delorean[ %s  %s ]>' % (self._dt, self._tz)

    def __eq__(self):
        pass

    def __getattr__(self, name):
        """
        Implement __getattr__ to call `last` or `first` when function does not
        exist
        """
        func_parts = name.split('_')

        if len(func_parts) != 2:
            raise AttributeError

        try:
            func = getattr(self, func_parts[0], None)
            if not func or func_parts[1] not in self._VALID_SHIFTS:
                raise AttributeError

            return func
        except:
            raise AttributeError

    def last(self, shift_by, shift_by_multiple=None):
        """
        Shift datetime back by some unit in _VALID_SHIFTS and shift that amount
        by some multiple, defined by shift_by_multiple
        """
        pass

    def next(self, shift_by, shift_by_multiple=None):
        """
        Shift datetime back by some unit in _VALID_SHIFTS and shift that amount
        by some multiple, defined by shift_by_multiple
        """
        pass

    def timezone(self):
        """
        Return a valid pytz timezone object or raises some error
        """
        if self._tz is None:
            return None
        try:
            return timezone(self._tz)
        except pytz.exceptions.UnknownTimeZoneError:
            # raise some delorean error
            pass

    def truncate(self, s):
        """
        Truncate the delorian object to the nearest s
        (second, minute, hour, day, month, year)
        """
        if s is 'second':
            self._dt = self._dt.replace(microsecond=0)
        elif s is 'minute':
            self._dt = self._dt.replace(second=0, microsecond=0)
        elif s is 'hour':
            self._dt = self._dt.replace(minute=0, second=0, microsecond=0)
        elif s is 'day':
            self._dt = self._dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif s is 'month':
            self._dt = self._dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif s is 'year':
            self._dt = self._dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            # raise some error
            pass

        return self

    def naive(self):
        """
        Returns a naive datetime object from the delorean object, this
        method simply removes tzinfo doesn't not cause a shift in time.
        """
        return self._dt.replace(tzinfo=None)

    def midnight(self, s):
        """
        return the particular midnight of the particular delorean object
        """
        self._dt = self._dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def date(self):
        """
        This method returns the actual date object associated with class
        """
        return self._dt.date

    @property
    def datetime(self):
        """
        This method returns the actual datetime object associated with class
        """
        return self._dt
