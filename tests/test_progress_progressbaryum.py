import locale

import pytest

from etaprogress import eta, progress_components
from etaprogress.progress import ProgressBarYum


@pytest.fixture(autouse=True, scope='module')
def define_locale():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def test_undefined():
    progress_components.DEFAULT_TERMINAL_WIDTH = 60
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarYum(None, '', max_width=55)

    assert '            [       ] --- KiB/s |   0.0 B              ' == progress_bar.bar
    assert '            [       ] --- KiB/s |   0.0 B              ' == progress_bar.bar
    assert '            [       ] --- KiB/s |   0.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(10)
    assert '            [       ] --- KiB/s |    10 B              ' == progress_bar.bar
    assert '            [       ] --- KiB/s |    10 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(100)
    assert '            [       ]   180 B/s |   100 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(1954727)
    assert '            [       ] 1.9 MiB/s | 1.9 MiB              ' == progress_bar.bar
    assert '            [       ] 1.9 MiB/s | 1.9 MiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(4217583)
    assert '            [       ] 2.8 MiB/s | 4.0 MiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(6826725)
    assert '            [       ] 3.4 MiB/s | 6.5 MiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(8659265)
    assert '            [       ] 3.6 MiB/s | 8.3 MiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.0
    progress_bar.eta.set_numerator(8659265)
    assert '            [       ] 3.3 MiB/s | 8.3 MiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.5
    progress_bar.eta.set_numerator(21057295)
    assert '            [       ] 4.8 MiB/s |  20 MiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868726.0
    progress_bar.eta.set_numerator(65572196)
    assert '            [       ]  10 MiB/s |  62 MiB              ' == progress_bar.bar

    progress_bar.done = True
    assert '                                |  62 MiB  00:00:05    ' == progress_bar.bar


def test_defined():
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarYum(2000, 'file.iso')

    assert 'file.iso   0% [          ] --- KiB/s |   0.0 B              ' == progress_bar.bar
    assert 'file.iso   0% [          ] --- KiB/s |   0.0 B              ' == progress_bar.bar
    assert 'file.iso   0% [          ] --- KiB/s |   0.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(102)
    assert 'file.iso   5% [-         ] --- KiB/s |   102 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(281)
    assert 'file.iso  14% [=         ]   358 B/s |   281 B  00:00:05 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(593)
    assert 'file.iso  29% [==-       ]   491 B/s |   593 B  00:00:03 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(1925)
    assert 'file.iso  96% [=========-] 1.1 KiB/s | 1.9 KiB  00:00:01 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(1999)
    assert 'file.iso  99% [=========-] 1.1 KiB/s | 2.0 KiB  00:00:01 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(2000)
    assert 'file.iso                             | 2.0 KiB  00:00:03    ' == progress_bar.bar


def test_defined_rounded():
    eta._NOW = lambda: 1411868723.5
    progress_bar = ProgressBarYum(1023, 'long_file_name.iso')

    assert 'long_fil   0% [          ] --- KiB/s |   0.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(1022)
    assert 'long_fil  99% [=========-] --- KiB/s | 1.0 KiB              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(1023)
    assert 'long_file_name.iso                   | 1.0 KiB  00:00:01    ' == progress_bar.bar


def test_defined_hour():
    progress_bar = ProgressBarYum(2000, 'file.iso')

    assert 'file.iso   0% [          ] --- KiB/s |   0.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert 'file.iso   0% [          ] --- KiB/s |   1.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(2)
    assert 'file.iso   0% [          ]   0.5 B/s |   2.0 B  01:06:36 ETA' == progress_bar.bar


def test_defined_weeks():
    progress_bar = ProgressBarYum(2000000000, 'file.iso')

    assert 'file.iso   0% [          ] --- KiB/s |   0.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert 'file.iso   0% [          ] --- KiB/s |   1.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(2)
    assert 'file.i   0% [       ]   0.5 B/s |   2.0 B  1111111:06:36 ETA' == progress_bar.bar


def test_defined_wont_fit():
    progress_bar = ProgressBarYum(2000, 'file.iso', max_width=33)
    assert '   0% [] --- KiB/s |   0.0 B              ' == progress_bar.bar
    progress_bar.done = True
    assert 'file.iso  |   0.0 B  00:00:00    ' == progress_bar.bar

    progress_bar = ProgressBarYum(2000, 'file.iso', max_width=30)
    assert '   0% [] --- KiB/s |   0.0 B              ' == progress_bar.bar
    progress_bar.done = True
    assert 'file.i |   0.0 B  00:00:00    ' == progress_bar.bar

    progress_bar = ProgressBarYum(2000, 'file.iso', max_width=20)
    assert '   0% [] --- KiB/s |   0.0 B              ' == progress_bar.bar
    progress_bar.done = True
    assert ' |   0.0 B  00:00:00    ' == progress_bar.bar


def test_defined_long():
    progress_components.DEFAULT_TERMINAL_WIDTH = 50
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarYum(20, 'a.iso')

    assert 'a.is   0% [    ] --- KiB/s |   0.0 B              ' == progress_bar.bar
    assert 'a.is   0% [    ] --- KiB/s |   0.0 B              ' == progress_bar.bar
    assert 'a.is   0% [    ] --- KiB/s |   0.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert 'a.is   5% [    ] --- KiB/s |   1.0 B              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(2)
    assert 'a.is  10% [    ]   2.0 B/s |   2.0 B  00:00:09 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(3)
    assert 'a.is  15% [-   ]   2.0 B/s |   3.0 B  00:00:09 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(4)
    assert 'a.is  20% [-   ]   2.0 B/s |   4.0 B  00:00:08 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(5)
    assert 'a.is  25% [=   ]   2.0 B/s |   5.0 B  00:00:08 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(6)
    assert 'a.is  30% [=   ]   2.0 B/s |   6.0 B  00:00:07 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868725.0
    progress_bar.eta.set_numerator(7)
    assert 'a.is  35% [=   ]   2.0 B/s |   7.0 B  00:00:07 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868725.5
    progress_bar.eta.set_numerator(8)
    assert 'a.is  40% [=-  ]   2.0 B/s |   8.0 B  00:00:06 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868726.0
    progress_bar.eta.set_numerator(9)
    assert 'a.is  45% [=-  ]   2.0 B/s |   9.0 B  00:00:06 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868726.5
    progress_bar.eta.set_numerator(10)
    assert 'a.is  50% [==  ]   2.0 B/s |    10 B  00:00:05 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(11)
    assert 'a.is  55% [==  ]   2.0 B/s |    11 B  00:00:05 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868727.5
    progress_bar.eta.set_numerator(12)
    assert 'a.is  60% [==  ]   2.0 B/s |    12 B  00:00:04 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868728.0
    progress_bar.eta.set_numerator(13)
    assert 'a.is  65% [==- ]   2.0 B/s |    13 B  00:00:04 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868728.5
    progress_bar.eta.set_numerator(14)
    assert 'a.is  70% [==- ]   2.0 B/s |    14 B  00:00:03 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868729.0
    progress_bar.eta.set_numerator(15)
    assert 'a.is  75% [=== ]   2.0 B/s |    15 B  00:00:03 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868729.5
    progress_bar.eta.set_numerator(16)
    assert 'a.is  80% [=== ]   2.0 B/s |    16 B  00:00:02 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868730.0
    progress_bar.eta.set_numerator(17)
    assert 'a.is  85% [=== ]   2.0 B/s |    17 B  00:00:02 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868730.5
    progress_bar.eta.set_numerator(18)
    assert 'a.is  90% [===-]   2.0 B/s |    18 B  00:00:01 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868731.0
    progress_bar.eta.set_numerator(19)
    assert 'a.is  95% [===-]   2.0 B/s |    19 B  00:00:01 ETA' == progress_bar.bar

    eta._NOW = lambda: 1411868731.5
    progress_bar.eta.set_numerator(20)
    assert 'a.iso                      |    20 B  00:00:10    ' == progress_bar.bar
