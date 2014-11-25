#!/usr/bin/env python
"""Example implementation of ProgressBarWget. Does not save to file.

This example application downloads a specified file to null. Its only purpose
is to show a progress bar and ETA similar to that of the wget application.

Usage:
    example_wget.py [--ignore-length] <url>

Options:
    --ignore-length         Ignore `Content-Length' header field.
"""

from __future__ import print_function
import locale
import os
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
    """Downloads the file, but doesn't save it (just the file size)."""

    def __init__(self, response):
        super(DownloadThread, self).__init__()
        self.response = response

        self._bytes_downloaded = 0
        self.daemon = True

    def run(self):
        for chunk in self.response.iter_content(1024):
            self._bytes_downloaded += len(chunk)

    @property
    def bytes_downloaded(self):
        """Read-only interface to _bytes_downloaded."""
        return self._bytes_downloaded


def main():
    """From: http://stackoverflow.com/questions/20801034/how-to-measure-download-speed-and-progress-using-requests"""
    # Prepare.
    if os.name == 'nt':
        locale.setlocale(locale.LC_ALL, 'english-us')
    else:
        locale.resetlocale()
    response = requests.get(OPTIONS['<url>'], stream=True)
    content_length = None if OPTIONS['--ignore-length'] else int(response.headers.get('Content-Length'))
    progress_bar = ProgressBarWget(content_length, eta_every=4)
    thread = DownloadThread(response)
    print_every_seconds = 0.25

    # Download.
    thread.start()
    while True:
        progress_bar.numerator = thread.bytes_downloaded
        print(progress_bar, end='\r')
        sys.stdout.flush()

        # For undefined downloads (no content-length), check if thread has stopped. Loop only checks defined downloads.
        if not thread.isAlive():
            progress_bar.force_done = True
            break
        if progress_bar.done:
            break

        time.sleep(print_every_seconds)
    print(progress_bar)  # Always print one last time.


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *_: error('', 0))  # Properly handle Control+C
    main()
