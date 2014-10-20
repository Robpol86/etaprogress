# etaprogress

Draw progress bars with room for colors and display rates and ETAs in your console applications. ETA library is its own
class so it may be used in other non-console applications. ETAs calculated with simple linear regression.

`etaprogress` is supported on Python 2.6, 2.7, 3.3, and 3.4.

[![Build Status](https://travis-ci.org/Robpol86/etaprogress.svg?branch=master)]
(https://travis-ci.org/Robpol86/etaprogress)
[![Coverage Status](https://img.shields.io/coveralls/Robpol86/etaprogress.svg)]
(https://coveralls.io/r/Robpol86/etaprogress)
[![Latest Version](https://pypip.in/version/etaprogress/badge.png)]
(https://pypi.python.org/pypi/etaprogress/)
[![Downloads](https://pypip.in/download/etaprogress/badge.png)]
(https://pypi.python.org/pypi/etaprogress/)
[![Download format](https://pypip.in/format/etaprogress/badge.png)]
(https://pypi.python.org/pypi/etaprogress/)
[![License](https://pypip.in/license/etaprogress/badge.png)]
(https://pypi.python.org/pypi/etaprogress/)

## Quickstart

Install:
```bash
pip install etaprogress
```

## Example Implementations

![Example Scripts Screenshot](/example.gif?raw=true "Example Scripts Screenshot")

Source code for examples: [example.py](example.py), [example_colors.py](example_colors.py),
and [example_wget.py](example_wget.py)

## Usage

If all you need is a progress bar with an ETA, you only have to import a class in the `etaprogress.progress` module.

### Simple Usage

> These examples are intended for python2.7.

```python
import time
from etaprogress.progress import ProgressBar
total = 5
bar = ProgressBar(total, max_width=40)
for i in range(total + 1):
    bar.numerator = i
    print bar
    time.sleep(1)
```

```
  0% (0/5) [               ] eta --:-- -
 20% (1/5) [###            ] eta 00:05 \
 40% (2/5) [######         ] eta 00:04 |
 60% (3/5) [#########      ] eta 00:03 /
 80% (4/5) [############   ] eta 00:02 -
100% (5/5) [###############] eta 00:00 \
```

Of course that's not a very good progress bar animation. Here's a better one with `print_function`:

```python
from __future__ import print_function
import sys
import time
from etaprogress.progress import ProgressBar
total = 5
bar = ProgressBar(total, max_width=40)
for i in range(total + 1):
    bar.numerator = i
    print(bar, end='\r')
    sys.stdout.flush()
    time.sleep(1)
print()
```

```
100% (5/5) [###############] eta 00:00 \
```

### Terminal Colors Support

Colors are supported using [colorclass](https://github.com/Robpol86/colorclass). Take a look at
[example_colors.py](example_colors.py) on how to implement colorful progress bars. You may have to subclass one of the
ProgressBar classes (or even BaseProgressBar) to add colors to every nook and cranny of a progress bar.

### Class Attributes

There are five different progress bar classes with visual differences:

* `ProgressBar` -- a simple progress bar.
* `ProgressBarBits` -- similar to `ProgressBar` but converts numbers to bits, kilobits, etc.
* `ProgressBarBytes` -- similar to `ProgressBar` but converts numbers to bytes, kibibytes (kilobytes), etc.
* `ProgressBarWget` -- a progress bar that looks like the one in the GNU `wget` application.
* `ProgressBarYum` -- a progress bar that looks like the one in CentOS/RHEL 7 YUM utility.

Below is a list of attributes available (though not necessarily used, e.g. not all show rates) to all classes.

Name | Description/Notes
:--- | :----------------
`max_width` | Limit number of characters shown (by default the full progress bar takes up the entire terminal width).
