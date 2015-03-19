etaprogress
===========

Draw progress bars with room for colors and display rates and ETAs in your console applications. ETA library is its own
class so it may be used in other non-console applications. ETAs calculated with simple linear regression.

This library supports both defined and undefined progress bars. Undefined progress bars are those that do not have a
"total size". Similar to when wget downloads a file with an unknown file size. Due to this, undefined progress bars
have no percent and no ETA. Defined progress bars are the usual progress bars with percentages and ETAs.

* Python 2.6, 2.7, 3.3, and 3.4 supported on Linux and OS X.
* Python 2.7, 3.3, and 3.4 supported on Windows (both 32 and 64 bit versions of Python).

Tested on Windows XP and Windows 10 technical preview.

.. image:: https://img.shields.io/appveyor/ci/Robpol86/etaprogress.svg?style=flat-square
   :target: https://ci.appveyor.com/project/Robpol86/etaprogress
   :alt: Build Status Windows

.. image:: https://img.shields.io/travis/Robpol86/etaprogress/master.svg?style=flat-square
   :target: https://travis-ci.org/Robpol86/etaprogress
   :alt: Build Status

.. image:: https://img.shields.io/codecov/c/github/Robpol86/etaprogress/master.svg?style=flat-square
   :target: https://codecov.io/github/Robpol86/etaprogress
   :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/etaprogress.svg?style=flat-square
   :target: https://pypi.python.org/pypi/etaprogress/
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/etaprogress.svg?style=flat-square
   :target: https://pypi.python.org/pypi/etaprogress/
   :alt: Downloads

Quickstart
----------

Install:

.. code:: bash

    pip install etaprogress


Example Implementations
-----------------------

.. image:: /example.gif?raw=true
   :alt: Example Scripts Screenshot

Source code for examples: `example.py <example.py>`_, `example_colors.py <example_colors.py>`_,
and `example_wget.py <example_wget.py>`_

Usage
-----

If all you need is a progress bar with an ETA, you only have to import a class in the ``etaprogress.progress`` module.
To get the progress bar itself just cast to string or print the instance.

Simple Usage
````````````

.. code:: python

    import time
    from etaprogress.progress import ProgressBar
    total = 5
    bar = ProgressBar(total, max_width=40)
    for i in range(total + 1):
        bar.numerator = i
        print bar
        time.sleep(1)

.. code::

      0% (0/5) [               ] eta --:-- -
     20% (1/5) [###            ] eta 00:05 \
     40% (2/5) [######         ] eta 00:04 |
     60% (3/5) [#########      ] eta 00:03 /
     80% (4/5) [############   ] eta 00:02 -
    100% (5/5) [###############] eta 00:00 \

Of course that's not a very good progress bar animation. Here's a better one with ``print_function``:

.. code:: python

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

.. code::

    100% (5/5) [###############] eta 00:00 \

Terminal Colors Support
```````````````````````

Colors are supported using `colorclass <https://github.com/Robpol86/colorclass>`_. Take a look at
`example_colors.py <example_colors.py>`_ on how to implement colorful progress bars. You may have to subclass one of the
ProgressBar classes (or even BaseProgressBar) to add colors to every nook and cranny of a progress bar.

Class Attributes
````````````````

There are five different progress bar classes with visual differences:

* ``ProgressBar`` -- a simple progress bar.
* ``ProgressBarBits`` -- similar to ``ProgressBar`` but converts numbers to bits, kilobits, etc.
* ``ProgressBarBytes`` -- similar to ``ProgressBar`` but converts numbers to bytes, kibibytes (kilobytes), etc.
* ``ProgressBarWget`` -- a progress bar that looks like the one in the GNU ``wget`` application.
* ``ProgressBarYum`` -- a progress bar that looks like the one in CentOS/RHEL 7 ``yum`` utility.

============== =============================================================================================================================
Name           Description/Notes
============== =============================================================================================================================
``max_width``  Limit number of characters shown (by default the full progress bar takes up the entire terminal width).
``eta_every``  Calculate and cache the ETA string after this many numerator setting iteration. Default is every iter.
``force_done`` For undefined progress bars this indicates that the progress has completed.
``filename``   'ProgressBarYum' only. The string to display before the progress bar. Limited to whatever space is available in the terminal.
============== =============================================================================================================================

Class Properties
````````````````

=============== =======================================================================================================================================================
Name            Description/Notes
=============== =======================================================================================================================================================
``denominator`` Returns the denominator of the progress bars. The same value provided when instantiating.
``done``        Returns True if the progress has completed.
``numerator``   Read/write. Returns the numerator as an integer or sets a new numerator. When setting a numerator it must be equal to or greater than the previous one.
``percent``     Returns the percent as a float.
``rate``        Returns the rate of the progress as a float.
``undefined``   Return True if the progress bar is undefined.
=============== =======================================================================================================================================================

Changelog
---------

1.1.0
`````

* Added Windows support.

1.0.0
`````

* Initial release.
