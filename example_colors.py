#!/usr/bin/env python
"""Example implementation of ProgressBar with color text.

Requires colorclass (pip install colorclass).

Usage:
    example_colors.py run [--light-bg]
    example_colors.py run -h | --help

Options:
    -h --help       Show this screen.
    --light-bg      Autocolors adapt to white/light backgrounds.
"""

from __future__ import print_function
import locale
import signal
import sys
import time

from colorclass import Color, set_dark_background, set_light_background
from docopt import docopt
from etaprogress.progress import ProgressBar

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def error(message, code=1):
    """Prints an error message to stderr and exits with a status of 1 by default."""
    if message:
        print('ERROR: {0}'.format(message), file=sys.stderr)
    else:
        print(file=sys.stderr)
    sys.exit(code)


def main():
    # Prepare.
    locale.resetlocale()
    progress_bar = ProgressBar(100)
    progress_bar.bar.CHAR_FULL = Color('{autoyellow}#{/autoyellow}')
    progress_bar.bar.CHAR_LEADING = Color('{autoyellow}#{/autoyellow}')
    progress_bar.bar.CHAR_LEFT_BORDER = Color('{autoblue}[{/autoblue}')
    progress_bar.bar.CHAR_RIGHT_BORDER = Color('{autoblue}]{/autoblue}')

    # Run.
    for i in range(101):
        progress_bar.numerator = i
        print(progress_bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    print(progress_bar)  # Always print one last time.


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *_: error('', 0))  # Properly handle Control+C
    set_light_background() if OPTIONS['--light-bg'] else set_dark_background()
    main()
