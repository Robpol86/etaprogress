"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from decimal import Decimal, ROUND_DOWN
import locale

from etaprogress.components.bars import Bar, BarDoubled, BarUndefinedAnimated, BarUndefinedEmpty
from etaprogress.components.base_progress_bar import BaseProgressBar
from etaprogress.components.eta_conversions import eta_hms, eta_letters
from etaprogress.components.misc import get_remaining_width, SPINNER
from etaprogress.components.units import UnitBit, UnitByte

__all__ = ('ProgressBar', 'ProgressBarBits', 'ProgressBarBytes', 'ProgressBarWget', 'ProgressBarYum')


class ProgressBar(BaseProgressBar):
    """Draw a progress bar showing the ETA, percentage, done/total items, and a spinner.

    Looks like one of these:
      8% (  8/100) [##                                  ] eta 00:24 /
    100% (100/100) [####################################] eta 00:01 -
    23 [                       ?                        ] eta --:-- |
    """

    def __init__(self, denominator, max_width=None):
        super(ProgressBar, self).__init__(denominator, max_width=max_width)
        if self.undefined:
            self.template = '{numerator} {bar} eta --:-- {spinner}'
            self.bar = BarUndefinedAnimated()
        else:
            self.template = '{percent:3d}% ({fraction}) {bar} eta {eta} {spinner}'
            self.bar = Bar()

    def __str__(self):
        """Returns the fully-built progress bar and other data."""
        # Partially build out template.
        bar = '{bar}'
        spinner = next(SPINNER)
        if self.undefined:
            numerator = self.str_numerator
            template = self.template.format(numerator=numerator, bar=bar, spinner=spinner)
        else:
            percent = int(self.percent)
            fraction = self.str_fraction
            eta = self._eta_string or '--:--'
            template = self.template.format(percent=percent, fraction=fraction, bar=bar, eta=eta, spinner=spinner)

        # Determine bar width and finish.
        width = get_remaining_width(template.format(bar=''), self.max_width or None)
        bar = self.bar.bar(width, percent=self.percent)
        return template.format(bar=bar)

    @staticmethod
    def _generate_eta(seconds):
        """Returns a human readable ETA string."""
        return '' if seconds is None else eta_hms(seconds, always_show_minutes=True)

    @property
    def str_fraction(self):
        """Returns the fraction with additional whitespace."""
        if self.undefined:
            return None
        denominator = locale.format('%d', self.denominator, grouping=True)
        numerator = self.str_numerator.rjust(len(denominator))
        return '{0}/{1}'.format(numerator, denominator)

    @property
    def str_numerator(self):
        """Returns the numerator as a formatted string."""
        return locale.format('%d', self.numerator, grouping=True)


class ProgressBarBits(ProgressBar):
    """Draw a progress bar showing the ETA, percentage, done/total items, a spinner, and units in bits.

    Looks like one of these:
      7% (  7.40/100.00 mb) [#                          ] eta 00:20 \
    100% (100.00/100.00 mb) [###########################] eta 00:00 \
    62.96 mb [                               ?          ] eta --:-- |
    """

    def __init__(self, denominator, max_width=None):
        super(ProgressBarBits, self).__init__(denominator, max_width)
        self._unit_class = UnitBit

    @property
    def str_fraction(self):
        """Returns the fraction with additional whitespace."""
        if self._eta.undefined:
            return None

        # Determine denominator and its unit.
        unit_denominator, unit = self._unit_class(self.denominator).auto
        formatter = '%d' if unit_denominator == self.denominator else '%0.2f'
        denominator = locale.format(formatter, unit_denominator, grouping=True)

        # Determine numerator.
        unit_numerator = getattr(self._unit_class(self.numerator), unit)
        if self.done:
            rounded_numerator = unit_numerator
        else:
            rounded_numerator = float(Decimal(str(unit_numerator)).quantize(Decimal('.01'), rounding=ROUND_DOWN))
        numerator = locale.format(formatter, rounded_numerator, grouping=True).rjust(len(denominator))

        return '{0}/{1} {2}'.format(numerator, denominator, unit)

    @property
    def str_numerator(self):
        """Returns the numerator with formatting."""
        if not self.undefined:
            return None
        unit_numerator, unit = self._unit_class(self.numerator).auto
        formatter = '%d' if unit_numerator == self.numerator else '%0.2f'
        numerator = locale.format(formatter, unit_numerator, grouping=True)
        return '{0} {1}'.format(numerator, unit)


class ProgressBarBytes(ProgressBarBits):
    """Draw a progress bar showing the ETA, percentage, done/total items, a spinner, and units in bytes.

    Looks like one of these:
      7% ( 7.06/95.37 MiB) [##                          ] eta 00:20 \
    100% (95.37/95.37 MiB) [############################] eta 00:00 |
    24.72 MiB [                     ?                   ] eta --:-- -
    """

    def __init__(self, denominator, max_width=None):
        super(ProgressBarBytes, self).__init__(denominator, max_width)
        self._unit_class = UnitByte


class ProgressBarWget(BaseProgressBar):
    """Progress bar modeled after the one in wget.

    Looks like one of these:
    35% [=======>               ] 35,802,443  4.66MiB/s  eta 14s
    100%[======================>] 100,000,000 4.59MiB/s   in 21s
        [                  <=>  ] 22,222,206  4.65MiB/s
        [  <=>                  ] 100,000,000 4.59MiB/s   in 21s
    """

    _Bar__CHAR_UNIT_FULL = '='
    _Bar__CHAR_UNIT_LEADING = '>'
    _Bar__CHARS_UNDEFINED_ANIMATED = '<=>'

    def __init__(self, denominator, max_width=None, eta_every=1):
        """Positional arguments:
        denominator -- the final unit (Content Length, final size, etc.). None if unknown.

        Keyword arguments:
        max_width -- limit final output to this width instead of terminal width.
        eta_every -- if 4, then every 4th .bar iteration changes the ETA displayed.
        """
        super(ProgressBarWget, self).__init__(denominator, max_width=max_width, eta_every=eta_every)
        if self.undefined:
            self.template = '    {bar} {numerator:<11s} {rate:>9s}  {eta:<12s}'
            BarUndefinedAnimated.CHAR_ANIMATED = '<=>'
            self.bar = BarUndefinedAnimated()
        else:
            self.template = '{percent:^4s}{bar} {numerator:<11s} {rate:>9s}  {eta:<12s}'
            Bar.CHAR_FULL = '='
            Bar.CHAR_LEADING = '>'
            self.bar = Bar()

    def __str__(self):
        """Returns the fully-built progress bar and other data."""
        # Partially build out template.
        bar = '{bar}'
        numerator = locale.format('%d', self.numerator, grouping=True)
        rate = self.str_rate
        eta = self.str_eta
        if self.undefined:
            template = self.template.format(bar=bar, numerator=numerator, rate=rate, eta=eta)
        else:
            percent = '{0}%'.format(int(self.percent))
            template = self.template.format(percent=percent, bar=bar, numerator=numerator, rate=rate, eta=eta)

        # Determine bar width and finish.
        width = get_remaining_width(template.format(bar=''), self.max_width or None)
        bar = self.bar.bar(width, percent=self.percent)
        return template.format(bar=bar)

    @staticmethod
    def _generate_eta(seconds):
        """Returns a human readable ETA string."""
        return '' if seconds is None else eta_letters(seconds)

    @property
    def str_eta(self):
        """Returns a formatted ETA value for the progress bar."""
        eta = eta_letters(self._eta.elapsed) if self.done else self._eta_string
        if not eta:
            return ''
        if eta.count(' ') > 1:
            eta = ' '.join(eta.split(' ')[:2])  # Only show up to two units (h and m, no s for example).
        return (' in {0}' if self.done else 'eta {0}').format(eta)

    @property
    def str_rate(self):
        """Returns the rate with formatting. If done, returns the overall rate instead."""
        # Handle special cases.
        if not self._eta.started or self._eta.stalled or not self.rate:
            return '--.-KiB/s'

        unit_rate, unit = UnitByte(self._eta.rate_overall if self.done else self.rate).auto
        if unit_rate >= 100:
            formatter = '%d'
        elif unit_rate >= 10:
            formatter = '%.1f'
        else:
            formatter = '%.2f'
        return '{0}{1}/s'.format(locale.format(formatter, unit_rate, grouping=False), unit)


class ProgressBarYum(BaseProgressBar):
    """Progress bar modeled after the one in YUM.

    Looks like one of these:
    CentOS-7.0  27% [===-         ] 265 MiB/s | 1.8 GiB  00:00:19 ETA
    CentOS-7.0-1406-x86_64-Everything.iso     | 6.6 GiB  00:00:26
    CentOS-7.0      [             ] 265 MiB/s | 2.8 GiB
    """

    def __init__(self, denominator, filename, max_width=None):
        """Positional arguments:
        denominator -- the final unit (Content Length, final size, etc.). None if unknown.

        Keyword arguments:
        max_width -- limit final output to this width instead of terminal width.
        """
        super(ProgressBarYum, self).__init__(denominator, max_width=max_width)
        self.filename = filename
        self.template = '{filename} {percent:>4s} {bar} {rate:>9s} | {numerator:>7s}  {eta:<12s}'
        self.template_completed = '{filename} | {numerator:>7s}  {eta:<12s}'
        if self.undefined:
            self.bar = BarUndefinedEmpty()
        else:
            self.bar = BarDoubled()

    def __str__(self):
        """Returns the fully-built progress bar and other data."""
        # Partially build out template.
        filename = '{filename}'
        numerator = self.str_numerator
        eta = self.str_eta
        if self.done:
            template = self.template_completed.format(filename=filename, numerator=numerator, eta=eta)
        else:
            bar = '{bar}'
            percent = '' if self.undefined else '{0}%'.format(int(self.percent))
            rate = self.str_rate
            template = self.template.format(filename=filename, percent=percent, bar=bar, rate=rate, numerator=numerator,
                                            eta=eta)
        width = get_remaining_width(template.format(bar='', filename=''), self.max_width or None)

        # Filename will have 40% of the available width if not done.
        if self.done:
            filename = self.filename[:width].ljust(width) if width > 0 else ''
            bar = None
        else:
            width_filename = int(width * 0.4)
            filename = self.filename[:width_filename].ljust(width_filename) if width_filename > 0 else ''
            bar = self.bar.bar(width - width_filename, percent=self.percent)
        return template.format(bar=bar, filename=filename)

    @staticmethod
    def _generate_eta(seconds):
        """Returns a human readable ETA string."""
        return '' if seconds is None else eta_hms(seconds, always_show_hours=True, hours_leading_zero=True)

    @property
    def str_eta(self):
        """Returns a formatted ETA value for the progress bar."""
        if self.done:
            return eta_hms(self._eta.elapsed, always_show_hours=True, hours_leading_zero=True)
        if not self._eta_string:
            return ''
        return '{0} ETA'.format(self._eta_string)

    @property
    def str_numerator(self):
        """Returns the numerator with formatting."""
        unit_numerator, unit = UnitByte(self.numerator).auto_no_thousands
        if unit_numerator >= 10:
            formatter = '%d'
        else:
            formatter = '%0.1f'
        return '{0} {1}'.format(locale.format(formatter, unit_numerator, grouping=False), unit)

    @property
    def str_rate(self):
        """Returns the rate with formatting."""
        # Handle special cases.
        if not self._eta.started or self._eta.stalled or not self.rate:
            return '--- KiB/s'

        unit_rate, unit = UnitByte(self.rate).auto_no_thousands
        if unit_rate >= 10:
            formatter = '%d'
        else:
            formatter = '%0.1f'
        return '{0} {1}/s'.format(locale.format(formatter, unit_rate, grouping=False), unit)
