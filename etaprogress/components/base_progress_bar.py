"""Base class for all progress bars (including other data like rates and ETA)."""

from etaprogress.eta import ETA


class BaseProgressBar(object):
    """Holds common properties/methods/etc for ProgressBar and related subclasses."""

    def __init__(self, denominator, max_width=None, eta_every=1):
        self._eta = ETA(denominator=denominator)
        self.max_width = max_width
        self.eta_every = eta_every
        self._eta_string = ''
        self._eta_count = 1

    @staticmethod
    def _generate_eta(seconds):
        raise NotImplementedError

    @property
    def numerator(self):
        """Returns the numerator as an integer."""
        return int(self._eta.numerator)

    @numerator.setter
    def numerator(self, value):
        """Sets a new numerator and generates the ETA. Must be greater than or equal to previous numerator."""
        # If ETA is every iteration, don't do anything fancy.
        if self.eta_every <= 1:
            self._eta.numerator = value
            self._eta_string = self._generate_eta(self._eta.eta_seconds)
            return

        # Calculate if this iteration is the right one.
        if self._eta_count >= self.eta_every:
            self._eta_count = 1
            self._eta.numerator = value
            self._eta_string = self._generate_eta(self._eta.eta_seconds)
            return

        self._eta_count += 1
        self._eta.set_numerator(value, calculate=False)

    @property
    def percent(self):
        """Returns the percent as a float."""
        return float(self._eta.percent)

    @property
    def rate(self):
        """Returns the rate of the progress as a float. Selects the unstable rate if eta_every > 1 for performance."""
        # If ETA is every iteration, don't do anything fancy.
        return float(self._eta.rate_unstable if self.eta_every > 1 else self._eta.rate)
