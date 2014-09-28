"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from datetime import datetime
import time


class ETA(object):
    """Calculates the estimated time remaining."""

    SCOPE_LAST_SECONDS = 60

    def __init__(self, denominator):
        self.denominator = denominator
        self.done = False
        self._data = dict()  # Keys are numerators, values are time.time() (Unix epoch).
        self._now = lambda: time.time()  # For testing.

    def increment(self, numerator, timestamp=None):
        """'Increments' the numerator (number of items done). Also cleans up timing data.

        This method may be used to set new increments or update the current numerator.

        Positional arguments:
        numerator -- the new numerator to add to the timing data.

        Keyword arguments:
        timestamp -- optionally override the time the numerator changed. Defaults to right now.
        """
        # Validate
        latest = sorted(self._data.items())[-1] if self._data else (None, None)
        now = self._now()
        if self._data and numerator < latest[0]:
            raise ValueError('cannot edit past numerators.')
        if self._data and timestamp is not None and timestamp < latest[1]:
            raise ValueError('timestamp may not decrement.')
        if self._data and timestamp is not None and timestamp > now:
            raise ValueError('timestamp must not be in the future.')

        # Update data.
        self._data[numerator] = timestamp or now

        # Filter old data.
        self._data = dict((k, v) for k, v in self._data.items() if now - v <= self.SCOPE_LAST_SECONDS)

    def stalled(self, timeout=5):
        """Returns True if no data has been added in the last 5 (default timeout) seconds."""
        if not self._data:
            return True
        latest = sorted(self._data.items())[-1]
        return time.time() - latest[1] >= timeout

    @property
    def eta_datetime(self):
        """Returns a datetime object representing the ETA or None if there is no data yet."""
        if not self._data:
            return None
        latest = sorted(self._data.items())[-1]
        remaining = self.denominator - latest[0]
        rate = self.rate
        seconds_left = remaining / rate
        return datetime.fromtimestamp(latest[1] + seconds_left)

    @property
    def eta_seconds(self):
        """Returns the ETA in seconds or None if there is no data yet."""
        if not self._data:
            return None
        latest = sorted(self._data.items())[-1]
        remaining = self.denominator - latest[0]
        rate = self.rate
        return remaining / rate

    @property
    def rate(self):
        """Returns the rate (numerator units per second)."""
        return None  # TODO


class ProgressBar(object):
    """Builds a basic progress bar similar to the one in wget."""

    BAR_LEADING_CHAR = '>'
    BAR_MAIN_CHAR = '='
    TEMPLATE = '{percent:3d}% [{bar}] {total} {rate}  eta {eta}'