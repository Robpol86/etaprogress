#!/usr/bin/env python
"""Example implementation of ProgressBarWget. Does not save to file.

This example application downloads a specified file to null. Its only purpose
is to show a progress bar and ETA similar to that of the wget application.

Usage:
    example_wget.py [--ignore-length] [--limit-rate=RATE] <url>

Options:
    --ignore-length         Ignore `Content-Length' header field.
    --limit-rate=RATE       Limit download rate to RATE (e.g. 20k or 1m, these
                            are in bytes).
"""

from __future__ import print_function
import signal
import sys

from docopt import docopt
from etaprogress.progress import ProgressBarWget

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def error(message, code=1):
    """Prints an error message to stderr and exits with a status of 1 by default."""
    if message:
        print('ERROR: {}'.format(message), file=sys.stderr)
    else:
        print(file=sys.stderr)
    sys.exit(code)


def download(rate):
    """File download logic.
    From: http://stackoverflow.com/questions/20801034/how-to-measure-download-speed-and-progress-using-requests
    """
    pass


def main():
    # Parse rate.
    if OPTIONS['--limit-rate']:
        rate = int(''.join([c for c in OPTIONS['--limit-rate'] if c.isdigit()]))
        if OPTIONS['--limit-rate'].endswith('k'):
            rate *= 1024
        elif OPTIONS['--limit-rate'].endswith('m'):
            rate *= 1048576
        print('Limiting to {0} bytes per second.'.format(rate))
    else:
        rate = None

    # Download.
    download(rate)

    print('Done downloading.')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *_: error('', 0))  # Properly handle Control+C
    main()
