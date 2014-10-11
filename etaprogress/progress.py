"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from decimal import Decimal, ROUND_DOWN
from itertools import cycle
import locale

from etaprogress.eta import ETA
from etaprogress.progress_components import Bar, BaseProgressBar, EtaHMS, Spinner, UnitBit, UnitByte


class ProgressBar(Bar, EtaHMS, Spinner, BaseProgressBar):
    """Draw a progress bar showing the ETA, percentage, done/total items, and a spinner.

    Looks like one of these:
     90% ( 90/100) [###############################   ] eta 1:00:00 \
    100% (100/100) [#################################  ] eta  00:00 |
    100 [     ?                                         ] eta --:-- /
    100% (100/100) [###################################] eta  00:00 |
    100 [                    ?                          ] eta --:-- /
    """

    TEMPLATE = '{percent:3d}% ({fraction}) {bar} eta {eta} {spinner}'
    TEMPLATE_UNDEFINED = '{numerator} {bar} eta --:-- {spinner}'

    def __init__(self, denominator, max_width=None):
        """Positional arguments:
        denominator -- the final unit (Content Length, final size, etc.). None if unknown.

        Keyword arguments:
        unit -- convert numerator/denominator to these units (e.g. '', 'bits', 'bytes').
        """
        eta = ETA(denominator=denominator)
        self.eta = eta
        self.max_width = max_width
        Bar.__init__(self, undefined_animated=eta.undefined)
        EtaHMS.__init__(self, always_show_minutes=True)
        Spinner.__init__(self)

    @property
    def fraction(self):
        """Returns the fraction with additional whitespace."""
        denominator = locale.format('%d', self.eta.denominator, grouping=True)
        numerator = locale.format('%d', self.eta.numerator, grouping=True).rjust(len(denominator))
        return '{0}/{1}'.format(numerator, denominator)

    @property
    def numerator(self):
        """Returns the numerator with formatting."""
        return locale.format('%d', self.eta.numerator, grouping=True)

    @property
    def bar(self):
        """Generates and returns the progress bar (one-line string)."""
        template = self.TEMPLATE_UNDEFINED if self.eta.undefined else self.TEMPLATE
        values = dict(
            percent=int(self.eta.percent),
            numerator='',
            fraction='',
            bar='',
            eta='--:--',
            spinner=getattr(self, '_Spinner__spinner'),  # Apparently PyCharm doesn't support name mangling.
        )

        # Fill in ETA, fraction, and numerator.
        seconds = self.eta.eta_seconds
        if not self.eta.undefined and seconds is not None:
            values['eta'] = getattr(self, '_EtaHMS__eta')(seconds)
        if not self.eta.undefined:
            values['fraction'] = self.fraction
        else:
            values['numerator'] = self.numerator

        # Fill in bar.
        width = getattr(self, '_BaseProgressBar__get_remaining_width')(template, values, self.max_width)
        values['bar'] = getattr(self, '_Bar__bar')(width, self.eta.percent)
        return template.format(**values)


class ProgressBarBits(ProgressBar):
    """Draw a progress bar showing the ETA, percentage, done/total items, a spinner, and units in bits.

    Looks like one of these:
     90% ( 90.00/100.00 kb) [######################   ] eta 1:00:00 \
    100% (100.00/100.00 kb) [########################  ] eta  00:00 |
    100.00 kb [     ?                                   ] eta --:-- /
    100% (100.00/100.00 kb) [##########################] eta  00:00 |
    100.00 kb [                 ?                       ] eta --:-- /
    """

    def __init__(self, denominator, max_width=None):
        super(ProgressBarBits, self).__init__(denominator, max_width)
        self._unit_class = UnitBit

    @property
    def fraction(self):
        """Returns the fraction with additional whitespace."""
        # Determine denominator and its unit.
        unit_denominator, unit = self._unit_class(self.eta.denominator).auto
        formatter = '%d' if unit_denominator == self.eta.denominator else '%0.2f'
        denominator = locale.format(formatter, unit_denominator, grouping=True)
        max_len = len(denominator) if unit_denominator == self.eta.denominator else 8

        # Determine numerator.
        unit_numerator = getattr(self._unit_class(self.eta.numerator), unit)
        if self.eta.done:
            rounded_numerator = unit_numerator
        else:
            rounded_numerator = float(Decimal(unit_numerator).quantize(Decimal('.01'), rounding=ROUND_DOWN))
        numerator = locale.format(formatter, rounded_numerator, grouping=True).rjust(max_len)

        return '{0}/{1} {2}'.format(numerator, denominator, unit)

    @property
    def numerator(self):
        """Returns the numerator with formatting."""
        unit_numerator, unit = self._unit_class(self.eta.numerator).auto
        formatter = '%d' if unit_numerator == self.eta.numerator else '%0.2f'
        numerator = locale.format(formatter, unit_numerator, grouping=True)
        return '{0} {1}'.format(numerator, unit)


class ProgressBarBytes(ProgressBarBits):
    """Draw a progress bar showing the ETA, percentage, done/total items, a spinner, and units in bytes.

    Looks like one of these:
     90% ( 90.00/100.00 KiB) [######################   ] eta 1:00:00 \
    100% (100.00/100.00 KiB) [########################  ] eta  00:00 |
    100.00 KiB [     ?                                   ] eta --:-- /
    100% (100.00/100.00 KiB) [##########################] eta  00:00 |
    100.00 KiB [                 ?                       ] eta --:-- /
    """

    def __init__(self, denominator, max_width=None):
        super(ProgressBarBits, self).__init__(denominator, max_width)
        self._unit_class = UnitByte


# Everything below this line is incomplete.


class ProgressBarWget(ProgressBar):
    """Progress bar modeled after the one in wget.

    Looks like one of these:
     1% [                             ] 1,133,490   1.05MiB/s
    33% [========>                    ] 35,248,370  9.46MiB/s  eta 10s
    33% [========>                    ] 35,248,370  9.46MiB/s  eta 2m 10s
    100%[============================>] 104,874,307 14.3MiB/s   in 9.7s
        [      <=>                    ] 35,248,370  9.46MiB/s
        [                   <=>       ] 35,248,370  --.-KiB/s   in 9.7s
    """
    BAR_LEADING_CHAR = '>'
    BAR_MAIN_CHAR = '='
    TEMPLATE = '{percent:3d}% [{bar}] {total} {rate}  eta {eta}'


class ProgressBarYum(ProgressBar):
    """Progress bar modeled after the one in YUM.

    Looks like one of these:
    filename.iso   99% [============-] 294 KiB/s | 407 KiB    00:03 ETA
    file.iso        9% [==           ] 294 KiB/s | 407 KiB    00:03 ETA
    no_length.iso      [             ] 294 KiB/s | 407 KiB
    stalled.iso        [             ] --- KiB/s | 407 KiB
    """