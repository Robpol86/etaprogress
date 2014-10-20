#!/usr/bin/env python
"""Example implementation of all progress bars.

Usage:
    example_colors.py progress_bar [--undefined]
    example_colors.py progress_bar_bits [--undefined]
    example_colors.py progress_bar_bytes [--undefined]
    example_colors.py progress_bar_wget [--undefined]
    example_colors.py progress_bar_yum [--undefined]
    example_colors.py -h | --help

Options:
    -h --help       Show this screen.
    --undefined     Show undefined progress bars instead.
"""

from __future__ import print_function
import locale
import signal
import sys
import time

from docopt import docopt
from etaprogress.progress import ProgressBar, ProgressBarBits, ProgressBarBytes, ProgressBarWget, ProgressBarYum

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def error(message, code=1):
    """Prints an error message to stderr and exits with a status of 1 by default."""
    if message:
        print('ERROR: {0}'.format(message), file=sys.stderr)
    else:
        print(file=sys.stderr)
    sys.exit(code)


def progress_bar():
    bar = ProgressBar(0 if OPTIONS['--undefined'] else 100)
    for i in range(101):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.force_done = True  # Needed in case of --undefined.
    print(bar)  # Always print one last time.


def progress_bar_bits():
    bar = ProgressBarBits(0 if OPTIONS['--undefined'] else 100000000)
    for i in range(0, 100000001, 1234567):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.numerator = 100000000
    bar.force_done = True
    print(bar)


def progress_bar_bytes():
    bar = ProgressBarBytes(0 if OPTIONS['--undefined'] else 100000000)
    for i in range(0, 100000001, 1234567):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.numerator = 100000000
    bar.force_done = True
    print(bar)


def progress_bar_wget():
    bar = ProgressBarWget(0 if OPTIONS['--undefined'] else 100000000)
    for i in range(0, 100000001, 1234567):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.numerator = 100000000
    bar.force_done = True
    print(bar)


def progress_bar_yum():
    files = {
        'CentOS-7.0-1406-x86_64-DVD.iso': 4148166656,
        'CentOS-7.0-1406-x86_64-Everything.iso': 7062159360,
        'md5sum.txt': 486,
    }
    for file_name, file_size in files.items():
        bar = ProgressBarYum(0 if OPTIONS['--undefined'] else file_size, file_name)
        for i in range(0, file_size + 1, int(file_size / 100.0)):
            bar.numerator = i
            print(bar, end='\r')
            sys.stdout.flush()
            time.sleep(0.25)
        bar.numerator = file_size
        bar.force_done = True
        print(bar)


def main():
    locale.resetlocale()
    if OPTIONS['progress_bar']:
        progress_bar()
    elif OPTIONS['progress_bar_bits']:
        progress_bar_bits()
    elif OPTIONS['progress_bar_bytes']:
        progress_bar_bytes()
    elif OPTIONS['progress_bar_wget']:
        progress_bar_wget()
    elif OPTIONS['progress_bar_yum']:
        progress_bar_yum()
    else:
        raise RuntimeError


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *_: error('', 0))  # Properly handle Control+C
    main()
