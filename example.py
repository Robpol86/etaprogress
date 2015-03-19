#!/usr/bin/env python
"""Example implementation of all progress bars.

Usage:
    example_colors.py progress_bar [-f] [--undefined]
    example_colors.py progress_bar_bits [-f] [--undefined]
    example_colors.py progress_bar_bytes [-f] [--undefined]
    example_colors.py progress_bar_wget [-f] [--undefined]
    example_colors.py progress_bar_yum [-f] [--undefined]
    example_colors.py -h | --help

Options:
    -f --fast       Quickly run example (for testing).
    -h --help       Show this screen.
    --undefined     Show undefined progress bars instead.
"""

from __future__ import print_function
import locale
import os
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
    denominator = 5 if OPTIONS['--fast'] else 100
    bar = ProgressBar(0 if OPTIONS['--undefined'] else denominator)
    for i in range(denominator + 1):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.force_done = True  # Needed in case of --undefined.
    print(bar)  # Always print one last time.


def progress_bar_bits():
    denominator = 10 if OPTIONS['--fast'] else 100000000
    bar = ProgressBarBits(0 if OPTIONS['--undefined'] else denominator)
    for i in range(0, denominator + 1, 2 if OPTIONS['--fast'] else 1234567):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.numerator = denominator
    bar.force_done = True
    print(bar)


def progress_bar_bytes():
    denominator = 10 if OPTIONS['--fast'] else 100000000
    bar = ProgressBarBytes(0 if OPTIONS['--undefined'] else denominator)
    for i in range(0, denominator + 1, 2 if OPTIONS['--fast'] else 1234567):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.numerator = denominator
    bar.force_done = True
    print(bar)


def progress_bar_wget():
    denominator = 10 if OPTIONS['--fast'] else 100000000
    bar = ProgressBarWget(0 if OPTIONS['--undefined'] else denominator)
    for i in range(0, denominator + 1, 2 if OPTIONS['--fast'] else 1234567):
        bar.numerator = i
        print(bar, end='\r')
        sys.stdout.flush()
        time.sleep(0.25)
    bar.numerator = denominator
    bar.force_done = True
    print(bar)


def progress_bar_yum():
    files = {
        'CentOS-7.0-1406-x86_64-DVD.iso': 10 if OPTIONS['--fast'] else 4148166656,
        'CentOS-7.0-1406-x86_64-Everything.iso': 15 if OPTIONS['--fast'] else 7062159360,
        'md5sum.txt': 5 if OPTIONS['--fast'] else 486,
    }
    for file_name, file_size in files.items():
        bar = ProgressBarYum(0 if OPTIONS['--undefined'] else file_size, file_name)
        for i in range(0, file_size + 1, 2 if OPTIONS['--fast'] else int(file_size / 100.0)):
            bar.numerator = i
            print(bar, end='\r')
            sys.stdout.flush()
            time.sleep(0.25)
        bar.numerator = file_size
        bar.force_done = True
        print(bar)


def main():
    if os.name == 'nt':
        locale.setlocale(locale.LC_ALL, 'english-us')
    else:
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
