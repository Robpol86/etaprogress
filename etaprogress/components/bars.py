"""Code for the actual progress bars themselves go here."""


class BarUndefinedEmpty(object):
    """Simplest progress bar. Just a static empty bar."""

    CHAR_LEFT_BORDER = '['
    CHAR_RIGHT_BORDER = ']'
    CHAR_EMPTY = ' '

    def __init__(self):
        self._width_offset = len(self.CHAR_LEFT_BORDER) + len(self.CHAR_RIGHT_BORDER)

    def bar(self, width, **_):
        """Returns the completed progress bar.

        Positional arguments:
        width -- the width of the entire bar (including borders).
        """
        return self.CHAR_LEFT_BORDER + self.CHAR_EMPTY * (width - self._width_offset) + self.CHAR_RIGHT_BORDER


class BarUndefinedAnimated(BarUndefinedEmpty):
    """Progress bar with a character that moves back and forth."""

    CHAR_ANIMATED = '?'

    def __init__(self):
        super(BarUndefinedAnimated, self).__init__()
        self._width_offset += len(self.CHAR_ANIMATED)
        self._position = -1
        self._direction = 1

    def bar(self, width, **_):
        """Returns the completed progress bar. Every time this is called the animation moves.

        Positional arguments:
        width -- the width of the entire bar (including borders).
        """
        width -= self._width_offset
        self._position += self._direction

        # Change direction.
        if self._position <= 0 and self._direction < 0:
            self._position = 0
            self._direction = 1
        elif self._position > width:
            self._position = width - 1
            self._direction = -1

        final_bar = (
            self.CHAR_LEFT_BORDER +
            self.CHAR_EMPTY * self._position +
            self.CHAR_ANIMATED +
            self.CHAR_EMPTY * (width - self._position) +
            self.CHAR_RIGHT_BORDER
        )
        return final_bar


class Bar(BarUndefinedEmpty):
    """A regular progress bar."""

    CHAR_FULL = '#'
    CHAR_LEADING = '#'

    def bar(self, width, percent=0):
        """Returns the completed progress bar.

        Positional arguments:
        width -- the width of the entire bar (including borders).

        Keyword arguments:
        percent -- the percentage to draw.
        """
        width -= self._width_offset
        units = int(percent * 0.01 * width)
        if not units:
            return self.CHAR_LEFT_BORDER + self.CHAR_EMPTY * width + self.CHAR_RIGHT_BORDER

        final_bar = (
            self.CHAR_LEFT_BORDER +
            self.CHAR_FULL * (units - 1) +
            self.CHAR_LEADING +
            self.CHAR_EMPTY * (width - units) +
            self.CHAR_RIGHT_BORDER
        )
        return final_bar


class BarDoubled(BarUndefinedEmpty):
    """A doubled progress bar. Shows different characters for half units."""

    CHAR_FULL = '='
    CHAR_HALF = '-'

    def bar(self, width, percent=0):
        """Returns the completed progress bar.

        Positional arguments:
        width -- the width of the entire bar (including borders).

        Keyword arguments:
        percent -- the percentage to draw.
        """
        width -= self._width_offset
        units_float = percent * 0.01 * width
        if units_float < 0.5:
            return self.CHAR_LEFT_BORDER + self.CHAR_EMPTY * width + self.CHAR_RIGHT_BORDER
        units = int(units_float)
        show_half = units_float - units >= 0.5

        if show_half:
            final_bar = (
                self.CHAR_LEFT_BORDER +
                self.CHAR_FULL * units +
                self.CHAR_HALF +
                self.CHAR_EMPTY * (width - units - 1) +
                self.CHAR_RIGHT_BORDER
            )
        else:
            final_bar = (
                self.CHAR_LEFT_BORDER +
                self.CHAR_FULL * units +
                self.CHAR_EMPTY * (width - units) +
                self.CHAR_RIGHT_BORDER
            )

        return final_bar
