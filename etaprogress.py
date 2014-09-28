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
        self.eta_epoch = None  # Estimated intercept of y=denominator. The 'x' in y = m * x + b.
        self.rate = 0.0  # Slope of the linear regression line. The 'm' in y = m * x + b.
        self._now = time.time  # For testing.
        self._timing_data = list()  # List of tuples. First item in tuple (x) is time.time(), second (y) is numerator.

    def set_numerator(self, numerator, calculate=True):
        """Sets the new numerator (number of items done). Also cleans up timing data and performs ETA calculation.

        Positional arguments:
        numerator -- the new numerator to add to the timing data.

        Keyword arguments:
        calculate -- calculate the ETA and rate by default.
        """
        # Validate
        if self._timing_data and numerator < self._timing_data[-1][1]:
            raise ValueError('numerator cannot decrement.')

        # Update data.
        self._timing_data.append((self._now(), numerator))

        # If done stop here.
        if self.done:
            return

        # Filter old data.
        if len(self._timing_data) > self.SCOPE_NUMBER_OF_ENTRIES:
            self._timing_data[:] = self._timing_data[-self.SCOPE_NUMBER_OF_ENTRIES:]

        # Calculate ETA and rate.
        if calculate and self.started:
            self._calculate()

    def _calculate(self):
        """Perform the ETA and rate calculation.

        http://code.activestate.com/recipes/578914-simple-linear-regression-with-pure-python/
        http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
        """
        # Calculate means and standard deviations.
        mean_x = sum(i[0] for i in self._timing_data) / len(self._timing_data)
        mean_y = sum(i[1] for i in self._timing_data) / len(self._timing_data)
        std_x = sqrt(sum(pow(i[0] - mean_x, 2) for i in self._timing_data) / (len(self._timing_data) - 1))
        std_y = sqrt(sum(pow(i[1] - mean_y, 2) for i in self._timing_data) / (len(self._timing_data) - 1))

        # Calculate coefficient.
        sum_xy, sum_sq_v_x, sum_sq_v_y = 0, 0, 0
        for x, y in self._timing_data:
            x -= mean_x
            y -= mean_y
            sum_xy += x * y
            sum_sq_v_x += pow(x, 2)
            sum_sq_v_y += pow(y, 2)
        pearson_r = sum_xy / sqrt(sum_sq_v_x * sum_sq_v_y)

        # Calculate line. y = mx + b where m is the slope and b is the y-intercept.
        y = self.denominator
        m = pearson_r * (std_y / std_x)
        b = mean_y - m * mean_x
        x = (y - b) / m
        self.rate = m
        self.eta_epoch = x

    @property
    def done(self):
        """Returns True if numerator == denominator."""
        return self.numerator == self.denominator

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
        return self._timing_data[-1][1]

    @property
    def stalled(self):
        """Returns True if the rate is 0."""
        return float(self.rate or 0) == 0.0

    @property
    def started(self):
        """Returns True if there is enough data to calculate the rate."""
        return len(self._timing_data) >= 2


class ProgressBar(object):
    """Builds a basic progress bar similar to the one in wget."""

    BAR_LEADING_CHAR = '>'
    BAR_MAIN_CHAR = '='
    TEMPLATE = '{percent:3d}% [{bar}] {total} {rate}  eta {eta}'
