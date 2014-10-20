"""Miscellaneous classes/functions/etc."""

import fcntl
from itertools import cycle
import struct
import termios
import time

DEFAULT_TERMINAL_WIDTH = None
NOW = time.time
SPINNER = cycle(('/', '-', '\\', '|'))


def terminal_width():
    """Returns the terminal's width (number of character columns)."""
    try:
        return struct.unpack('hhhh', fcntl.ioctl(0, termios.TIOCGWINSZ, '\000' * 8))[1]
    except IOError:
        if DEFAULT_TERMINAL_WIDTH is None:
            raise
        return int(DEFAULT_TERMINAL_WIDTH)


def get_remaining_width(sample_string, max_terminal_width=None):
    """Returns the number of characters available if sample string were to be printed in the terminal.

    Positional arguments:
    sample_string -- gets the length of this string.

    Keyword arguments:
    max_terminal_width -- limit the overall width of everything to these many characters.

    Returns:
    Integer.
    """
    if max_terminal_width is not None:
        available_width = min(terminal_width(), max_terminal_width)
    else:
        available_width = terminal_width()
    return available_width - len(sample_string)
