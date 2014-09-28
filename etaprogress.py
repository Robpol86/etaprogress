"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from datetime import datetime
import time


class ETA(object):
    """Calculates the estimated time remaining using linear regression."""

    SCOPE_LAST_SECONDS = 60

    def __init__(self, denominator):
        self.denominator = denominator
        self.done = False
        self._timing_data = dict()  # Keys are numerators, values are time.time() (Unix epoch).
        self._latest = (None, None)  # Updated by increment().
        self._now = time.time  # For testing.

    def increment(self, numerator, timestamp=None):
        """'Increments' the numerator (number of items done). Also cleans up timing data.

        This method may be used to set new increments or update the current numerator.

        Positional arguments:
        numerator -- the new numerator to add to the timing data.

        Keyword arguments:
        timestamp -- optionally override the time the numerator changed. Defaults to right now.
        """
        # Validate
        now = self._now()
        if self._timing_data and numerator < self._latest[0]:
            raise ValueError('cannot edit past numerators.')
        if self._timing_data and timestamp is not None and timestamp < self._latest[1]:
            raise ValueError('timestamp may not decrement.')
        if self._timing_data and timestamp is not None and timestamp > now:
            raise ValueError('timestamp must not be in the future.')

        # Filter old data.
        if self._timing_data:
            self._timing_data = dict((k, v) for k, v in self._timing_data.items() if now - v <= self.SCOPE_LAST_SECONDS)

        # Update data.
        value = timestamp or now
        self._timing_data[numerator] = value
        self._latest = (numerator, value)

    def stalled(self, timeout=5):
        """Returns True if no data has been added in the last 5 (default timeout) seconds."""
        if not self._timing_data:
            return True
        return self._now() - self._latest[1] >= timeout

    @property
    def eta_datetime(self):
        """Returns a datetime object representing the ETA or None if there is no data yet."""
        if not self._timing_data:
            return None
        return datetime.fromtimestamp(self._latest[1] + self.eta_seconds)

    @property
    def eta_seconds(self):
        """Returns the ETA in seconds or None if there is no data yet."""
        if not self._timing_data:
            return None
        remaining = self.denominator - self._latest[0]
        rate = self.rate
        return remaining / rate

    @property
    def numerator(self):
        """Returns the latest numerator."""
        if not self._timing_data:
            return None
        return self._latest[0]

    @property
    def rate(self):
        """Returns the rate (numerator units per second).

        Calculating the linear regression (like a trend-line).
        """
        return None  # TODO


class ProgressBar(object):
    """Builds a basic progress bar similar to the one in wget."""

    BAR_LEADING_CHAR = '>'
    BAR_MAIN_CHAR = '='
    TEMPLATE = '{percent:3d}% [{bar}] {total} {rate}  eta {eta}'