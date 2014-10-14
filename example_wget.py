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
import locale
import signal
import sys
import threading
import time

from docopt import docopt
from etaprogress.progress import ProgressBarWget
import requests

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def error(message, code=1):
    """Prints an error message to stderr and exits with a status of 1 by default."""
    if message:
        print('ERROR: {0}'.format(message), file=sys.stderr)
    else:
        print(file=sys.stderr)
    sys.exit(code)


class DownloadThread(threading.Thread):
    """Downloads the file, but doesn't save it (just the file size). Applies any rate limiting."""

    def __init__(self, response, rate):
        super(DownloadThread, self).__init__()
        self.response = response
        self.rate = rate

        self._bytes_downloaded = 0
        self.daemon = True

    def run(self):
        # TODO apply rate limiting.
        for chunk in self.response.iter_content(1024):
            self._bytes_downloaded += len(chunk)

    @property
    def bytes_downloaded(self):
        """Read-only interface to _bytes_downloaded."""
        return self._bytes_downloaded


def main():
    """From: http://stackoverflow.com/questions/20801034/how-to-measure-download-speed-and-progress-using-requests"""
    # TODO fix content length. Never stops.
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

    # Prepare.
    locale.resetlocale()
    response = requests.get(OPTIONS['<url>'], stream=True)
    content_length = None if OPTIONS['--ignore-length'] else int(response.headers.get('Content-Length'))
    progress_bar = ProgressBarWget(content_length, eta_every=4)
    thread = DownloadThread(response, rate)
    print_every_seconds = 0.25

    # Download.
    thread.start()
    while True:
        progress_bar.eta.numerator = thread.bytes_downloaded
        print(progress_bar.bar, end='\r')
        sys.stdout.flush()

        # For undefined downloads (no content-length), check if thread has stopped. Loop only checks defined downloads.
        if not thread.is_alive:
            progress_bar.done = True
            break
        if progress_bar.eta.done:
            break

        time.sleep(print_every_seconds)
    print(progress_bar.bar)  # Always print one last time.


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *_: error('', 0))  # Properly handle Control+C
    main()
