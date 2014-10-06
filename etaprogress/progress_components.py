"""Holds classes for different components of the ProgressBar class and friends.

Holds code for parts of the progress bar such as the spinner and calculating the progress bar itself.
"""

from __future__ import division
from itertools import cycle
import struct
import fcntl
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


class Spinner(object):
    """Holds logic for 'spinner' character."""

    __CHARS = ('/', '-', '\\', '|')

    def __init__(self, **_):
        super(Spinner, self).__init__()
        self.__iter = cycle(self.__CHARS)

    @property
    def __spinner(self):
        """Returns the spinner character. Every time this property is called a new character is returned."""
        return next(self.__iter)


class Unit(object):
    """Handles conversion from one unit (e.g. bytes) to another (e.g. gigabytes).

    Instance variables:
    __non_rate_unit -- dict of units and conversions for non-rate values.
    __rate_unit -- dict of units and conversions for rate values.
    """

    __DEFAULT = (
        (1, '', '/s'),
    )
    __BITS = (
        (1000000000000, 'tb', 'tbps'),
        (1000000000, 'gb', 'gbps'),
        (1000000, 'mb', 'mbps'),
        (1000, 'kb', 'kbps'),
        (1, 'b', 'bps'),
    )
    __BYTES = (
        (1099511627776, 'TiB', 'TiB/s'),
        (1073741824, 'GiB', 'GiB/s'),
        (1048576, 'MiB', 'MiB/s'),
        (1024, 'KiB', 'KiB/s'),
        (1, 'B', 'B/s'),
    )

    def __init__(self, __non_rate_unit='', __rate_unit='', **_):
        super(Unit, self).__init__()
        mapping = {
            '': self.__DEFAULT,
            'bits': self.__BITS,
            'bytes': self.__BYTES,
        }
        if __non_rate_unit not in mapping:
            raise ValueError('Invalid unit, must be: {0}'.format(', '.join(mapping)))
        if __rate_unit not in mapping:
            raise ValueError('Invalid rate unit, must be: {0}'.format(', '.join(mapping)))
        self.__non_rate_unit = mapping[__non_rate_unit]
        self.__rate_unit = mapping[__rate_unit]

    def __unit(self, value, rate=False, unit=None):
        """Converts `value` into another unit.

        Positional arguments:
        value -- the dividend in the formula.

        Keyword arguments:
        rate -- choose the rate units instead of non-rate (e.g. mbps instead of mb).
        unit -- automatic if None, override otherwise.

        Returns:
        Tuple of the converted value, the non-rate unit string, and the rate unit string.
        """
        unit_mapping = self.__rate_unit if rate else self.__non_rate_unit

        # Handle non-automatic unit.
        if unit is not None:
            selected = [r for r in unit_mapping if unit == r[2 if rate else 1]][0]
            return (value / selected[0]), selected[1], selected[2]

        # Handle automatic unit.
        for divisor, unit_str, unit_rate_str in unit_mapping:
            if divisor > value:
                continue
            return (value / divisor), unit_str, unit_rate_str

        # Handle 1 or 0 values.
        return (value / unit_mapping[-1][0]), unit_mapping[-1][1], unit_mapping[-1][2]


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

    def __init__(self, __shortest=False, __leading_zero=False, **_):
        super(EtaLetters, self).__init__()
        self.__shortest = __shortest
        self.__leading_zero = __leading_zero

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
        values['second'] = seconds

        # Map to characters.
        leading = lambda x: ('{0:02d}' if self.__leading_zero else '{0}').format(x)
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

    def __init__(self, __always_show_hours=False, __always_show_minutes=False, __hours_leading_zero=False, **_):
        super(EtaHMS, self).__init__()
        self.__always_show_hours = __always_show_hours
        self.__always_show_minutes = __always_show_minutes
        self.__hours_leading_zero = __hours_leading_zero

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
                template = '{hour:02d}:{minute:02d}:{second:02d}'
            else:
                template = '{hour}:{minute:02d}:{second:02d}'
        elif seconds >= 60 or self.__always_show_minutes:
            template = '{minute:02d}:{second:02d}'
        else:
            template = '{second:02d}'

        # Split up seconds into other units.
        if seconds >= 3600:
            values['hour'] = int(seconds / 3600.0)
            seconds -= values['hour'] * 3600
        if seconds >= 60:
            values['minute'] = int(seconds / 60.0)
            seconds -= values['minute'] * 60
        values['second'] = seconds

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

    def __init__(self, __with_leading=False, __undefined_animated=False, __undefined_empty=False, **_):
        super(Bar, self).__init__()
        self.__with_leading = __with_leading
        self.__undefined_animated = __undefined_animated
        self.__undefined_empty = __undefined_empty
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
    """."""

    @staticmethod
    def __get_remaining_width(template, values):
        """Calculates how much space is available for the progress bar itself.

        Positional arguments:
        template -- the string template to fill in.
        values -- the values to apply to the template.

        Returns:
        Number of characters available in the current terminal width.
        """
        return terminal_width() - len(template.format(**values))
