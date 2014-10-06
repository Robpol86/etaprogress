"""Easy to use ETA calculation and progress bar library.

https://github.com/Robpol86/etaprogress
https://pypi.python.org/pypi/etaprogress
"""

from __future__ import division
from itertools import cycle
import locale

from etaprogress.eta import ETA
from etaprogress.progress_components import Bar, BaseProgressBar, EtaHMS, Spinner


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


# Everything below this line is incomplete.


class ProgressBarBits(ProgressBar):
    pass


class ProgressBarBytes(ProgressBarBits):
    pass


class _BaseBar(object):
    """Base class for drawing a progress bar.

    Looks like one of these:
     90% [###############################  ]  1s left
    100% [#################################]  0s left
      0% [                                 ] 30m left
    1,282 [                                ]  no eta
    """
    pass



class ProgressBar2(object):
    """Progress bar object.

    Looks like one of these:
     90% ( 90/100 KiB) [###############################  ]  - stalled - \
    100% (100/100 KiB) [#################################] eta  0:00:00 |
    100 KiB [     ?                                      ] eta --:--:-- /
    100% (100/100) [#####################################] eta  0:00:00 |
    100 [                        ?                       ] eta --:--:-- /
    """

    TEMPLATE = '{percent:3d}% {fraction} [{bar}] {eta} {spinner}'
    TEMPLATE_UNDEFINED = '{numerator} [{bar}] eta --:-- {spinner}'

    def __init__(self, eta_instance, max_width=120, unit=None):
        self.eta_instance = eta_instance
        self.max_width = max_width
        self.min_width = 5
        self.spinner = cycle(self.SPINNER_CHARS)
        self.unit = unit or {'': 1}

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

        available_width = 0 - len(template.format(**answers))
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