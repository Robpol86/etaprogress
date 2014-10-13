"""Holds classes for different components of the ProgressBar class and friends.

Holds code for parts of the progress bar such as the spinner and calculating the progress bar itself.
"""

from __future__ import division
import fcntl
from itertools import cycle
from math import ceil
import struct
import termios

DEFAULT_TERMINAL_WIDTH = None


def terminal_width():
    """Returns the terminal's width (number of character columns)."""
    try:
        return struct.unpack('hhhh', fcntl.ioctl(0, termios.TIOCGWINSZ, '\000' * 8))[1]
    except IOError:
        if DEFAULT_TERMINAL_WIDTH is None:
            raise
        return int(DEFAULT_TERMINAL_WIDTH)


class UnitBit(object):
    """Converts bits into other units such as kilobits, megabits, etc."""

    def __init__(self, value):
        self._value = value

    @property
    def b(self):
        return self._value

    @property
    def kb(self):
        return self._value / 1000.0

    @property
    def mb(self):
        return self._value / 1000000.0

    @property
    def gb(self):
        return self._value / 1000000000.0

    @property
    def tb(self):
        return self._value / 1000000000000.0

    @property
    def auto(self):
        if self._value >= 1000000000000:
            return self.tb, 'tb'
        if self._value >= 1000000000:
            return self.gb, 'gb'
        if self._value >= 1000000:
            return self.mb, 'mb'
        if self._value >= 1000:
            return self.kb, 'kb'
        else:
            return self.b, 'b'


class UnitByte(object):
    """Converts bytes into other units such as kibibytes (like kilobytes, 1 * 1024)."""

    def __init__(self, value):
        self._value = value

    @property
    def B(self):
        return self._value

    @property
    def KiB(self):
        return self._value / 1024.0

    @property
    def MiB(self):
        return self._value / 1048576.0

    @property
    def GiB(self):
        return self._value / 1073741824.0

    @property
    def TiB(self):
        return self._value / 1099511627776.0

    @property
    def auto(self):
        if self._value >= 1099511627776:
            return self.TiB, 'TiB'
        if self._value >= 1073741824:
            return self.GiB, 'GiB'
        if self._value >= 1048576:
            return self.MiB, 'MiB'
        if self._value >= 1024:
            return self.KiB, 'KiB'
        else:
            return self.B, 'B'

    @property
    def auto_no_thousands(self):
        """Like self.auto but calculates the next unit if >999.99."""
        if self._value >= 1000000000000:
            return self.TiB, 'TiB'
        if self._value >= 1000000000:
            return self.GiB, 'GiB'
        if self._value >= 1000000:
            return self.MiB, 'MiB'
        if self._value >= 1000:
            return self.KiB, 'KiB'
        else:
            return self.B, 'B'


class Spinner(object):
    """Holds logic for 'spinner' character."""

    __CHARS = ('/', '-', '\\', '|')

    def __init__(self):
        self.__iter = cycle(self.__CHARS)

    @property
    def __spinner(self):
        """Returns the spinner character. Every time this property is called a new character is returned."""
        return next(self.__iter)


class EtaLetters(object):
    """Show the ETA using letters (e.g. '1s' or '5h 22m 2s').

    Instance variables:
    __shortest -- show the shortest possible string length by only showing the biggest unit.
    __leading_zero -- always show a leading zero for the minutes and seconds.
    """

    __CHARS_SECOND = 's'
    __CHARS_MINUTE = 'm'
    __CHARS_HOUR = 'h'
    __CHARS_DAY = 'd'
    __CHARS_WEEK = 'w'

    def __init__(self, shortest=False, leading_zero=False):
        self.__shortest = shortest
        self.__leading_zero = leading_zero

    def __eta(self, seconds):
        """Returns a string representing a human-readable ETA.

        Positional arguments:
        seconds -- number of seconds left (eta).

        Returns:
        ETA string (e.g. '1h 3s').
        """
        if not seconds:
            return '00s' if self.__leading_zero else '0s'

        # Split up seconds into other units.
        values = dict(week=0, day=0, hour=0, minute=0, second=0)
        if seconds >= 604800:
            values['week'] = int(seconds / 604800.0)
            seconds -= values['week'] * 604800
        if seconds >= 86400:
            values['day'] = int(seconds / 86400.0)
            seconds -= values['day'] * 86400
        if seconds >= 3600:
            values['hour'] = int(seconds / 3600.0)
            seconds -= values['hour'] * 3600
        if seconds >= 60:
            values['minute'] = int(seconds / 60.0)
            seconds -= values['minute'] * 60
        values['second'] = int(ceil(seconds))

        # Map to characters.
        leading = lambda x: ('{0:02.0f}' if self.__leading_zero else '{0}').format(x)
        mapped = (
            (self.__CHARS_WEEK, str(values['week'] or '')),
            (self.__CHARS_DAY, str(values['day'] or '')),
            (self.__CHARS_HOUR, str(values['hour'] or '')),
            (self.__CHARS_MINUTE, leading(values['minute']) if values['minute'] else ''),
            (self.__CHARS_SECOND, leading(values['second']) if values['second'] else ''),
        )
        trimmed = [(k, v) for k, v in mapped if v]
        formatted = ['{0}{1}'.format(v, k) for k, v in trimmed]

        return formatted[0] if self.__shortest else ' '.join(formatted)


class EtaHMS(object):
    """Show the ETA as ss, mm:ss, h:mm:ss, or hh:mm:ss.

    Instance variables:
    __always_show_hours -- don't hide the 0 hours.
    __always_show_minutes -- don't hide the 0 minutes.
    __hours_leading_zero -- show 01:00:00 instead of 1:00:00.
    """

    def __init__(self, always_show_hours=False, always_show_minutes=False, hours_leading_zero=False):
        self.__always_show_hours = always_show_hours
        self.__always_show_minutes = always_show_minutes
        self.__hours_leading_zero = hours_leading_zero

    def __eta(self, seconds):
        """Returns a string representing a human-readable ETA.

        Positional arguments:
        seconds -- number of seconds left (eta).

        Returns:
        ETA string (e.g. '01:59:59').
        """
        values = dict(hour=0, minute=0, second=0)
        if seconds >= 3600 or self.__always_show_hours:
            if self.__hours_leading_zero:
                template = '{hour:02.0f}:{minute:02.0f}:{second:02.0f}'
            else:
                template = '{hour}:{minute:02.0f}:{second:02.0f}'
        elif seconds >= 60 or self.__always_show_minutes:
            template = '{minute:02.0f}:{second:02.0f}'
        else:
            template = '{second:02.0f}'

        # Split up seconds into other units.
        if seconds >= 3600:
            values['hour'] = int(seconds / 3600.0)
            seconds -= values['hour'] * 3600
        if seconds >= 60:
            values['minute'] = int(seconds / 60.0)
            seconds -= values['minute'] * 60
        values['second'] = int(ceil(seconds))

        return template.format(**values)


class Bar(object):
    """Holds logic for a progress bar.

    Instance variables:
    __with_leading -- shows a leading character in the progress bar if True. Disables half unit.
    __undefined_animated -- progress bar will be undefined (no final size) with an animated character(s) every time
        _bar() is called (like wget) if True.
    __undefined_empty -- progress bar will be undefined and always empty with no animation if True.
    __undefined_animated_pos_addend -- offset the animated progress bar character(s) to this on the next iteration
        and the direction of the animated progress bar (1 or -1).
    """

    __CHARS_LEFT_BORDER = '['
    __CHARS_RIGHT_BORDER = ']'
    __CHARS_UNDEFINED_ANIMATED = '?'
    __CHAR_UNIT_LEADING = ' '
    __CHAR_UNIT_FULL = '#'
    __CHAR_UNIT_HALF = ' '
    __CHAR_UNIT_EMPTY = ' '

    def __init__(self, with_leading=False, undefined_animated=False, undefined_empty=False):
        self.__with_leading = with_leading
        self.__undefined_animated = undefined_animated
        self.__undefined_empty = undefined_empty
        self.__undefined_animated_pos_addend = (0, 1)

    def __bar(self, width, percent=None):
        """Returns a complete progress bar based on information provided.

        Positional arguments:
        width -- the width of the entire bar (including borders).

        Keyword arguments:
        percent -- percentage of the bar (0.0 - 100.0).

        Returns:
        Progress bar string (e.g. '[###     ]').
        """
        inner_width = width - (len(self.__CHARS_LEFT_BORDER) + len(self.__CHARS_RIGHT_BORDER))

        # Handle undefined progress bars.
        if self.__undefined_empty:
            inner_bar = self.__CHAR_UNIT_EMPTY * inner_width
            return self.__CHARS_LEFT_BORDER + inner_bar + self.__CHARS_RIGHT_BORDER
        if self.__undefined_animated:
            pos, addend = self.__undefined_animated_pos_addend
            char_len = len(self.__CHARS_UNDEFINED_ANIMATED)
            if addend > 0 and pos + char_len > inner_width:
                addend = -1
                pos = inner_width - char_len - 1
            elif addend < 0 and pos < 0:
                addend = 1
                pos = 1
            self.__undefined_animated_pos_addend = (pos + addend, addend)
            inner_bar = (pos * self.__CHAR_UNIT_EMPTY) + self.__CHARS_UNDEFINED_ANIMATED
            inner_bar = inner_bar.ljust(inner_width, self.__CHAR_UNIT_EMPTY)
            return self.__CHARS_LEFT_BORDER + inner_bar + self.__CHARS_RIGHT_BORDER

        # Handle empty defined progress bars.
        if percent is None or percent < 0 or percent > 100:
            raise ValueError('percent must be from 0 to 100.')
        show_blocks = inner_width * (percent / 100.0)
        show_half = False if self.__with_leading else (show_blocks - int(show_blocks)) >= 0.5
        if show_blocks < 0.5 or (not show_half and show_blocks < 1):
            inner_bar = self.__CHAR_UNIT_EMPTY * inner_width
            return self.__CHARS_LEFT_BORDER + inner_bar + self.__CHARS_RIGHT_BORDER

        # Handle defined progress bars with leading character.
        if self.__with_leading:
            inner_bar = (self.__CHAR_UNIT_FULL * (int(show_blocks) - 1)) + self.__CHAR_UNIT_LEADING
        else:
            inner_bar = (self.__CHAR_UNIT_FULL * int(show_blocks)) + (self.__CHAR_UNIT_HALF if show_half else '')
        inner_bar = inner_bar.ljust(inner_width, self.__CHAR_UNIT_EMPTY)
        return self.__CHARS_LEFT_BORDER + inner_bar + self.__CHARS_RIGHT_BORDER


class BaseProgressBar(object):
    """Holds common properties/methods/etc for ProgressBar and related subclasses."""

    @staticmethod
    def __get_remaining_width(template, values, max_terminal_width):
        """Calculates how much space is available for the progress bar itself.

        Positional arguments:
        template -- the string template to fill in.
        values -- the values to apply to the template.
        max_terminal_width -- limit maximum overall width. None disables limit.

        Returns:
        Number of characters available in the current terminal width.
        """
        if max_terminal_width is not None:
            available_width = min(terminal_width(), max_terminal_width)
        else:
            available_width = terminal_width()
        return available_width - len(template.format(**values))

    @property
    def __bar_with_dynamic_bar(self):
        """Returns a full progress bar. Fits in terminal or max_width if provided."""
        eta = getattr(self, 'eta')
        template = getattr(self, 'TEMPLATE_UNDEFINED') if eta.undefined else getattr(self, 'TEMPLATE')
        values = dict(
            bar='',
            eta=getattr(self, 'eta_string', None),
            fraction=getattr(self, 'fraction', None),
            numerator=getattr(self, 'numerator', None),
            percent=getattr(self, 'percent', None),
            rate=getattr(self, 'rate', None),
            spinner=getattr(self, 'spinner', None),
        )

        width = self.__get_remaining_width(template, values, getattr(self, 'max_width', None))
        values['bar'] = getattr(self, '_Bar__bar')(width, eta.percent)
        return template.format(**values)
