"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from itertools import cycle
import struct
import fcntl
import termios

from etaprogress.eta import ETA

DEFAULT_TERMINAL_WIDTH = None


def terminal_width():
    """Returns the terminal's width (number of character columns)."""
    try:
        return struct.unpack('hhhh', fcntl.ioctl(0, termios.TIOCGWINSZ, '\000' * 8))[1]
    except IOError:
        if DEFAULT_TERMINAL_WIDTH is None:
            raise
        return int(DEFAULT_TERMINAL_WIDTH)


class ProgressBar(object):
    """Progress bar object.

    Looks like either of these:
    100% (100/100 KiB) [#################################] eta  0:00:00 |
    100 KiB [     ?                            ] eta --:--:-- /
    """

    CHAR_BAR_LEADING = ''
    CHAR_BAR_MAIN = '#'
    CHAR_BAR_UNKNOWN = '?'
    CHAR_ETA = 'eta {0:2d}:{1:02d}:{2:02d}'
    CHAR_ETA_DASHED = 'eta --:--:--'
    CHAR_ETA_STALLED = ' - stalled -'
    SPINNER_CHARS = ('/', '-', '\\', '|')
    TEMPLATE = '{percent:3d}% {fraction} [{bar}] {eta} {spinner}'
    TEMPLATE_UNDEFINED = '{numerator} [{bar}] eta --:-- {spinner}'

    def __init__(self, denominator, max_width=120, unit=None):
        self.eta = ETA(denominator)
        self.max_width = max_width
        self.min_width = 5
        self.spinner = cycle(self.SPINNER_CHARS)
        self.unit = unit

    def __str__(self):
        return self.build_progress_bar()

    def displayed_eta(self):
        """Converts number of seconds remaining into mm:ss, h:mm:ss, or hh:mm:ss."""
        seconds = int(self.eta.eta_seconds)
        if not self.eta.started or seconds is None:
            return self.CHAR_ETA_DASHED
        if self.eta.stalled:
            return self.CHAR_ETA_STALLED

        hours, minutes = 0, 0
        if seconds > 3600:
            hours = int(seconds / 3600)
            seconds -= hours * 3600
        if seconds > 60:
            minutes = int(seconds / 60)
            seconds -= minutes * 60

        return self.CHAR_ETA.format(hours, minutes, seconds)

    def displayed_fraction(self):
        """Returns the fraction to display when the eta is not undefined."""
        if self.unit:
            return '({0}/{1})'.format(self.eta.numerator, self.eta.denominator)
        else:
            return '({0}/{1} {2})'.format(self.eta.numerator, self.eta.denominator, self.unit)

    def infer_info(self):
        """Infer information about the progress bar.

        Returns:
        Tuple, first item is the formatted string with {bar} left. Second item is available space for the bar.
        """
        answers = dict(
            percent=self.eta.percent,
            fraction=None,
            numerator=None,
            bar='',
            eta=None,
            spinner=next(self.spinner),
        )

        if self.eta.undefined:
            template = self.TEMPLATE_UNDEFINED
            answers['numerator'] = '{} {}'.format(self.eta.numerator, self.unit) if self.unit else self.eta.numerator
        else:
            template = self.TEMPLATE
            answers['fraction'] = self.displayed_fraction()
            answers['eta'] = self.displayed_eta()

        available_width = terminal_width() - len(template.format(**answers))
        answers['bar'] = '{bar}'
        return template.format(**answers), available_width

    def build_progress_bar(self):
        """Builds the progress bar to be passed to self.__str__().

        Returns:
        The completed progress bar (string).
        """
        proto_template, available_width = self.infer_info()
        width = max(min(available_width, self.max_width), self.min_width)
        # TODO


class ProgressBarWget(ProgressBar):
    BAR_LEADING_CHAR = '>'
    BAR_MAIN_CHAR = '='
    TEMPLATE = '{percent:3d}% [{bar}] {total} {rate}  eta {eta}'