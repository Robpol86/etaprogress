"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from datetime import datetime
from math import sqrt
import time

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '1.0.0'


class ETA(object):
    """Calculates the estimated time remaining using Simple Linear Regression."""

    SCOPE_NUMBER_OF_ENTRIES = 60

    def __init__(self, denominator):
        if denominator == 0:
            raise ValueError('denominator may not be zero.')
        if denominator < 0:
            raise ValueError('denominator must be positive/absolute.')
        self.denominator = denominator
        self.eta_epoch = None  # Estimated intercept of x=100. The 'y' in y = m * x + b.
        self.rate = None  # Slope of the linear regression line. The 'm' in y = m * x + b.
        self._latest = (None, None)  # Updated by set_numerator().
        self._now = time.time  # For testing.
        self._timing_data = dict()  # Keys (x) are numerators, values (y) are time.time() (Unix epoch).

    def set_numerator(self, numerator, timestamp=None, calculate=True):
        """Sets the new numerator (number of items done). Also cleans up timing data and performs ETA calculation.

        This method may also be used to update the current numerator.

        Positional arguments:
        numerator -- the new numerator to add to the timing data.

        Keyword arguments:
        timestamp -- optionally override the time the numerator changed. Defaults to right now.
        calculate -- calculate the ETA and rate by default.
        """
        # Validate
        now = self._now()
        if self._timing_data and numerator < self._latest[0]:
            raise ValueError('cannot edit past numerators.')
        if self._timing_data and timestamp is not None and timestamp < self._latest[1]:
            raise ValueError('timestamp may not decrement (slope must be positive).')
        if timestamp is not None and timestamp > now:
            raise ValueError('timestamp must not be in the future.')

        # Update data.
        value = timestamp or now
        self._latest = (numerator, value)
        self._timing_data[numerator] = value

        # Filter old data.
        if len(self._timing_data) > self.SCOPE_NUMBER_OF_ENTRIES:
            self._timing_data = dict(sorted(self._timing_data.items())[-self.SCOPE_NUMBER_OF_ENTRIES:])

        # Calculate ETA and rate.
        if calculate and len(self._timing_data) >= 2:
            self._calculate()

    def _calculate(self):
        """Perform the ETA and rate calculation.

        http://code.activestate.com/recipes/578914-simple-linear-regression-with-pure-python/
        http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
        """
        # Calculate means and standard deviations.
        timing_data = sorted(self._timing_data.items())
        mean_x = sum(i[0] for i in timing_data) / len(timing_data)
        mean_y = sum(i[1] for i in timing_data) / len(timing_data)
        std_x = sqrt(sum(pow(i[0] - mean_x, 2) for i in timing_data) / (len(timing_data) - 1))
        std_y = sqrt(sum(pow(i[1] - mean_y, 2) for i in timing_data) / (len(timing_data) - 1))

        # Calculate coefficient.
        sum_xy, sum_sq_v_x, sum_sq_v_y = 0, 0, 0
        for x, y in timing_data:
            x -= mean_x
            y -= mean_y
            sum_xy += x * y
            sum_sq_v_x += pow(x, 2)
            sum_sq_v_y += pow(y, 2)
        pearson_r = sum_xy / sqrt(sum_sq_v_x * sum_sq_v_y)

        # Calculate line. y = mx + b where m is the slope and b is the x-intercept.
        m = pearson_r * (std_y / std_x)
        b = mean_y - m * mean_x
        self.rate = m
        self.eta_epoch = (m * 100) + b

    @property
    def done(self):
        """Returns True if numerator == denominator."""
        return self._latest[0] == self.denominator

    @property
    def eta_datetime(self):
        """Returns a datetime object representing the ETA or None if there is no data yet."""
        if not self.eta_epoch:
            return None
        return datetime.fromtimestamp(self.eta_epoch)

    @property
    def eta_seconds(self):
        """Returns the ETA in seconds or None if there is no data yet."""
        if not self.eta_epoch:
            return None
        eta = self.eta_epoch - self._now()
        return eta if eta > 0 else 0

    @property
    def numerator(self):
        """Returns the latest numerator."""
        if not self._timing_data:
            return 0
        return self._latest[0]


class ProgressBar(object):
    """Builds a basic progress bar similar to the one in wget."""

    BAR_LEADING_CHAR = '>'
    BAR_MAIN_CHAR = '='
    TEMPLATE = '{percent:3d}% [{bar}] {total} {rate}  eta {eta}'
