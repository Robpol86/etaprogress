"""Holds classes for different components of the ProgressBar class and friends.

Holds code for parts of the progress bar such as the spinner and calculating the progress bar itself.
"""

from itertools import cycle


class Spinner(object):
    """Holds logic for 'spinner' character."""

    SPINNER_CHARS = ('/', '-', '\\', '|')

    def __init__(self):
        self._spinner_iter = cycle(self.SPINNER_CHARS)

    @property
    def _spinner(self):
        """Returns the spinner character. Every time this property is called a new character is returned."""
        return next(self._spinner_iter)


class Bar(object):
    """Holds logic for a progress bar.

    Instance variables:
    _with_leading -- shows a leading character in the progress bar if True. Disables half unit.
    _undefined_animated -- progress bar will be undefined (no final size) with an animated character(s) every time
        _bar() is called (like wget) if True.
    _undefined_empty -- progress bar will be undefined and always empty with no animation if True.
    _undefined_animated_pos_addend -- offset the animated progress bar character(s) to this on the next iteration and
        the direction of the animated progress bar (1 or -1).
    """

    CHARS_BAR_LEFT_BORDER = '['
    CHARS_BAR_RIGHT_BORDER = ']'
    CHARS_BAR_UNDEFINED_ANIMATED = '?'
    CHAR_BAR_UNIT_LEADING = ' '
    CHAR_BAR_UNIT_FULL = '#'
    CHAR_BAR_UNIT_HALF = ' '
    CHAR_BAR_UNIT_EMPTY = ' '

    def __init__(self, with_leading=False, undefined_animated=False, undefined_empty=False):
        self._with_leading = with_leading
        self._undefined_animated = undefined_animated
        self._undefined_empty = undefined_empty
        self._undefined_animated_pos_addend = (0, 1)

    def _bar(self, width, percent=None):
        """Returns a complete progress bar based on information provided.

        Positional arguments:
        width -- the width of the entire bar (including borders).
        percent -- percentage of the bar (0.0 - 100.0).
        """
        inner_width = width - (len(self.CHARS_BAR_LEFT_BORDER) + len(self.CHARS_BAR_RIGHT_BORDER))

        # Handle undefined progress bars.
        if self._undefined_empty:
            inner_bar = self.CHAR_BAR_UNIT_EMPTY * inner_width
            return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER
        if self._undefined_animated:
            pos, addend = self._undefined_animated_pos_addend
            char_len = len(self.CHARS_BAR_UNDEFINED_ANIMATED)
            if addend > 0 and pos + char_len > inner_width:
                addend = -1
                pos = inner_width - char_len - 1
            elif addend < 0 and pos < 0:
                addend = 1
                pos = 1
            self._undefined_animated_pos_addend = (pos + addend, addend)
            inner_bar = (pos * self.CHAR_BAR_UNIT_EMPTY) + self.CHARS_BAR_UNDEFINED_ANIMATED
            inner_bar = inner_bar.ljust(inner_width, self.CHAR_BAR_UNIT_EMPTY)
            return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER

        # Handle empty defined progress bars.
        if percent < 0 or percent > 100:
            raise ValueError('percent must be from 0 to 100.')
        show_blocks = inner_width * (percent / 100.0)
        show_half = False if self._with_leading else (show_blocks - int(show_blocks)) >= 0.5
        if show_blocks < 0.5 or (not show_half and show_blocks < 1):
            inner_bar = self.CHAR_BAR_UNIT_EMPTY * inner_width
            return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER

        # Handle defined progress bars with leading character.
        if self._with_leading:
            inner_bar = (self.CHAR_BAR_UNIT_FULL * (int(show_blocks) - 1)) + self.CHAR_BAR_UNIT_LEADING
        else:
            inner_bar = (self.CHAR_BAR_UNIT_FULL * int(show_blocks)) + (self.CHAR_BAR_UNIT_HALF if show_half else '')
        inner_bar = inner_bar.ljust(inner_width, self.CHAR_BAR_UNIT_EMPTY)
        return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER
