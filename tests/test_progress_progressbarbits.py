import locale

from etaprogress import eta, progress_components
from etaprogress.progress import ProgressBarBits


def test_undefined():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    progress_components.DEFAULT_TERMINAL_WIDTH = 50
    progress_bar = ProgressBarBits(None, max_width=30)

    assert '0 b [?           ] eta --:-- /' == progress_bar.bar
    assert '0 b [ ?          ] eta --:-- -' == progress_bar.bar
    assert '0 b [  ?         ] eta --:-- \\' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(10)
    assert '10 b [   ?       ] eta --:-- |' == progress_bar.bar
    assert '10 b [    ?      ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(100)
    assert '100 b [     ?    ] eta --:-- -' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(1954727)
    assert '1.95 mb [      ? ] eta --:-- \\' == progress_bar.bar
    assert '1.95 mb [       ?] eta --:-- |' == progress_bar.bar


def test_defined():
    progress_bar = ProgressBarBits(2000)

    assert '  0% (    0.00/2.00 kb) [            ] eta --:-- /' == progress_bar.bar
    assert '  0% (    0.00/2.00 kb) [            ] eta --:-- -' == progress_bar.bar
    assert '  0% (    0.00/2.00 kb) [            ] eta --:-- \\' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(102)
    assert '  5% (    0.10/2.00 kb) [            ] eta --:-- |' == progress_bar.bar
    assert '  5% (    0.10/2.00 kb) [            ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(281)
    assert ' 14% (    0.28/2.00 kb) [#           ] eta 00:05 -' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(593)
    assert ' 29% (    0.59/2.00 kb) [###         ] eta 00:03 \\' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(1925)
    assert ' 96% (    1.92/2.00 kb) [########### ] eta 00:00 |' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(1999)
    assert ' 99% (    1.99/2.00 kb) [########### ] eta 00:00 /' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(2000)
    assert '100% (    2.00/2.00 kb) [############] eta 00:00 -' == progress_bar.bar


def test_defined_rounded():
    progress_bar = ProgressBarBits(1999)

    assert '  0% (    0.00/2.00 kb) [            ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(1998)
    assert ' 99% (    1.99/2.00 kb) [########### ] eta --:-- -' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(1999)
    assert '100% (    2.00/2.00 kb) [############] eta --:-- \\' == progress_bar.bar


def test_defined_hour():
    progress_bar = ProgressBarBits(2000)

    assert '  0% (    0.00/2.00 kb) [            ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert '  0% (    0.00/2.00 kb) [            ] eta --:-- -' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(2)
    assert '  0% (    0.00/2.00 kb) [          ] eta 1:06:36 \\' == progress_bar.bar


def test_defined_wont_fit():
    progress_bar = ProgressBarBits(2000, max_width=33)
    assert '  0% (    0.00/2.00 kb) [] eta --:-- /' == progress_bar.bar

    progress_bar = ProgressBarBits(2000, max_width=30)
    assert '  0% (    0.00/2.00 kb) [] eta --:-- /' == progress_bar.bar


def test_defined_long():
    progress_components.DEFAULT_TERMINAL_WIDTH = 42
    progress_bar = ProgressBarBits(20)

    assert '  0% ( 0/20 b) [             ] eta --:-- /' == progress_bar.bar
    assert '  0% ( 0/20 b) [             ] eta --:-- -' == progress_bar.bar
    assert '  0% ( 0/20 b) [             ] eta --:-- \\' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert '  5% ( 1/20 b) [             ] eta --:-- |' == progress_bar.bar
    assert '  5% ( 1/20 b) [             ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(2)
    assert ' 10% ( 2/20 b) [#            ] eta 00:09 -' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(3)
    assert ' 15% ( 3/20 b) [#            ] eta 00:08 \\' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(4)
    assert ' 20% ( 4/20 b) [##           ] eta 00:08 |' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(5)
    assert ' 25% ( 5/20 b) [###          ] eta 00:08 /' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(6)
    assert ' 30% ( 6/20 b) [###          ] eta 00:07 -' == progress_bar.bar

    eta._NOW = lambda: 1411868725.0
    progress_bar.eta.set_numerator(7)
    assert ' 35% ( 7/20 b) [####         ] eta 00:06 \\' == progress_bar.bar

    eta._NOW = lambda: 1411868725.5
    progress_bar.eta.set_numerator(8)
    assert ' 40% ( 8/20 b) [#####        ] eta 00:06 |' == progress_bar.bar

    eta._NOW = lambda: 1411868726.0
    progress_bar.eta.set_numerator(9)
    assert ' 45% ( 9/20 b) [#####        ] eta 00:06 /' == progress_bar.bar

    eta._NOW = lambda: 1411868726.5
    progress_bar.eta.set_numerator(10)
    assert ' 50% (10/20 b) [######       ] eta 00:05 -' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(11)
    assert ' 55% (11/20 b) [#######      ] eta 00:04 \\' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(12)
    assert ' 60% (12/20 b) [#######      ] eta 00:04 |' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(13)
    assert ' 65% (13/20 b) [########     ] eta 00:03 /' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(14)
    assert ' 70% (14/20 b) [#########    ] eta 00:03 -' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(15)
    assert ' 75% (15/20 b) [#########    ] eta 00:02 \\' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(16)
    assert ' 80% (16/20 b) [##########   ] eta 00:02 |' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(17)
    assert ' 85% (17/20 b) [###########  ] eta 00:01 /' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(18)
    assert ' 90% (18/20 b) [###########  ] eta 00:01 -' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(19)
    assert ' 95% (19/20 b) [############ ] eta 00:00 \\' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(20)
    assert '100% (20/20 b) [#############] eta 00:00 |' == progress_bar.bar
