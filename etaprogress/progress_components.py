"""Holds classes for different components of the ProgressBar class and friends.

Holds code for parts of the progress bar such as the spinner and calculating the progress bar itself.
"""

from __future__ import division
from etaprogress.eta import ETA


class BaseProgressBar(object):
    """Holds common properties/methods/etc for ProgressBar and related subclasses."""

    def __init__(self, denominator, max_width=None, eta_every=1):
        self._eta = ETA(denominator=denominator)
        self.max_width = max_width
        self.eta_every = eta_every

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
