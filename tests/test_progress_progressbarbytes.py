from etaprogress import eta
from etaprogress.components import misc
from etaprogress.progress import ProgressBarBytes


def test_undefined():
    misc.terminal_width = lambda: 50
    progress_bar = ProgressBarBytes(None, max_width=30)

    assert '0 B [?           ] eta --:-- /' == str(progress_bar)
    assert '0 B [ ?          ] eta --:-- -' == str(progress_bar)
    assert '0 B [  ?         ] eta --:-- \\' == str(progress_bar)

    eta._NOW = lambda: 1411868722.0
    progress_bar.numerator = 10
    assert '10 B [   ?       ] eta --:-- |' == str(progress_bar)
    assert '10 B [    ?      ] eta --:-- /' == str(progress_bar)

    eta._NOW = lambda: 1411868722.5
    progress_bar.numerator = 100
    assert '100 B [     ?    ] eta --:-- -' == str(progress_bar)

    eta._NOW = lambda: 1411868723.0
    progress_bar.numerator = 1954727
    assert '1.86 MiB [      ?] eta --:-- \\' == str(progress_bar)
    assert '1.86 MiB [     ? ] eta --:-- |' == str(progress_bar)


def test_defined():
    progress_bar = ProgressBarBytes(2000)

    assert '  0% (0.00/1.95 KiB) [               ] eta --:-- /' == str(progress_bar)
    assert '  0% (0.00/1.95 KiB) [               ] eta --:-- -' == str(progress_bar)
    assert '  0% (0.00/1.95 KiB) [               ] eta --:-- \\' == str(progress_bar)

    eta._NOW = lambda: 1411868722.0
    progress_bar.numerator = 102
    assert '  5% (0.09/1.95 KiB) [               ] eta --:-- |' == str(progress_bar)
    assert '  5% (0.09/1.95 KiB) [               ] eta --:-- /' == str(progress_bar)

    eta._NOW = lambda: 1411868722.5
    progress_bar.numerator = 281
    assert ' 14% (0.27/1.95 KiB) [##             ] eta 00:05 -' == str(progress_bar)

    eta._NOW = lambda: 1411868723.0
    progress_bar.numerator = 593
    assert ' 29% (0.57/1.95 KiB) [####           ] eta 00:03 \\' == str(progress_bar)

    eta._NOW = lambda: 1411868723.5
    progress_bar.numerator = 1925
    assert ' 96% (1.87/1.95 KiB) [############## ] eta 00:01 |' == str(progress_bar)

    eta._NOW = lambda: 1411868724.0
    progress_bar.numerator = 1999
    assert ' 99% (1.95/1.95 KiB) [############## ] eta 00:01 /' == str(progress_bar)

    eta._NOW = lambda: 1411868724.5
    progress_bar.numerator = 2000
    assert '100% (1.95/1.95 KiB) [###############] eta 00:00 -' == str(progress_bar)
    assert '100% (1.95/1.95 KiB) [###############] eta 00:00 \\' == str(progress_bar)
    assert '100% (1.95/1.95 KiB) [###############] eta 00:00 |' == str(progress_bar)


def test_defined_rounded():
    progress_bar = ProgressBarBytes(1023)

    assert '  0% (    0/1,023 B) [               ] eta --:-- /' == str(progress_bar)

    eta._NOW = lambda: 1411868724.0
    progress_bar.numerator = 1022
    assert ' 99% (1,022/1,023 B) [############## ] eta --:-- -' == str(progress_bar)

    eta._NOW = lambda: 1411868724.5
    progress_bar.numerator = 1023
    assert '100% (1,023/1,023 B) [###############] eta --:-- \\' == str(progress_bar)
    assert '100% (1,023/1,023 B) [###############] eta --:-- |' == str(progress_bar)


def test_defined_hour():
    progress_bar = ProgressBarBytes(2000)

    assert '  0% (0.00/1.95 KiB) [               ] eta --:-- /' == str(progress_bar)

    eta._NOW = lambda: 1411868722.0
    progress_bar.numerator = 1
    assert '  0% (0.00/1.95 KiB) [               ] eta --:-- -' == str(progress_bar)

    eta._NOW = lambda: 1411868724.0
    progress_bar.numerator = 2
    assert '  0% (0.00/1.95 KiB) [             ] eta 1:06:36 \\' == str(progress_bar)


def test_defined_wont_fit():
    progress_bar = ProgressBarBytes(2000, max_width=33)
    assert '  0% (0.00/1.95 KiB) [] eta --:-- |' == str(progress_bar)

    progress_bar = ProgressBarBytes(2000, max_width=30)
    assert '  0% (0.00/1.95 KiB) [] eta --:-- /' == str(progress_bar)


def test_defined_long():
    misc.terminal_width = lambda: 42
    progress_bar = ProgressBarBytes(20)

    assert '  0% ( 0/20 B) [             ] eta --:-- -' == str(progress_bar)
    assert '  0% ( 0/20 B) [             ] eta --:-- \\' == str(progress_bar)

    eta._NOW = lambda: 1411868722.0
    progress_bar.numerator = 1
    assert '  5% ( 1/20 B) [             ] eta --:-- |' == str(progress_bar)
    assert '  5% ( 1/20 B) [             ] eta --:-- /' == str(progress_bar)

    eta._NOW = lambda: 1411868722.5
    progress_bar.numerator = 2
    assert ' 10% ( 2/20 B) [#            ] eta 00:09 -' == str(progress_bar)

    eta._NOW = lambda: 1411868723.0
    progress_bar.numerator = 3
    assert ' 15% ( 3/20 B) [#            ] eta 00:09 \\' == str(progress_bar)

    eta._NOW = lambda: 1411868723.5
    progress_bar.numerator = 4
    assert ' 20% ( 4/20 B) [##           ] eta 00:08 |' == str(progress_bar)

    eta._NOW = lambda: 1411868724.0
    progress_bar.numerator = 5
    assert ' 25% ( 5/20 B) [###          ] eta 00:08 /' == str(progress_bar)

    eta._NOW = lambda: 1411868724.5
    progress_bar.numerator = 6
    assert ' 30% ( 6/20 B) [###          ] eta 00:07 -' == str(progress_bar)

    eta._NOW = lambda: 1411868725.0
    progress_bar.numerator = 7
    assert ' 35% ( 7/20 B) [####         ] eta 00:07 \\' == str(progress_bar)

    eta._NOW = lambda: 1411868725.5
    progress_bar.numerator = 8
    assert ' 40% ( 8/20 B) [#####        ] eta 00:06 |' == str(progress_bar)

    eta._NOW = lambda: 1411868726.0
    progress_bar.numerator = 9
    assert ' 45% ( 9/20 B) [#####        ] eta 00:06 /' == str(progress_bar)

    eta._NOW = lambda: 1411868726.5
    progress_bar.numerator = 10
    assert ' 50% (10/20 B) [######       ] eta 00:05 -' == str(progress_bar)

    eta._NOW = lambda: 1411868727.0
    progress_bar.numerator = 11
    assert ' 55% (11/20 B) [#######      ] eta 00:05 \\' == str(progress_bar)

    eta._NOW = lambda: 1411868727.5
    progress_bar.numerator = 12
    assert ' 60% (12/20 B) [#######      ] eta 00:04 |' == str(progress_bar)

    eta._NOW = lambda: 1411868728.0
    progress_bar.numerator = 13
    assert ' 65% (13/20 B) [########     ] eta 00:04 /' == str(progress_bar)

    eta._NOW = lambda: 1411868728.5
    progress_bar.numerator = 14
    assert ' 70% (14/20 B) [#########    ] eta 00:03 -' == str(progress_bar)

    eta._NOW = lambda: 1411868729.0
    progress_bar.numerator = 15
    assert ' 75% (15/20 B) [#########    ] eta 00:03 \\' == str(progress_bar)

    eta._NOW = lambda: 1411868729.5
    progress_bar.numerator = 16
    assert ' 80% (16/20 B) [##########   ] eta 00:02 |' == str(progress_bar)

    eta._NOW = lambda: 1411868730.0
    progress_bar.numerator = 17
    assert ' 85% (17/20 B) [###########  ] eta 00:02 /' == str(progress_bar)

    eta._NOW = lambda: 1411868730.5
    progress_bar.numerator = 18
    assert ' 90% (18/20 B) [###########  ] eta 00:01 -' == str(progress_bar)

    eta._NOW = lambda: 1411868731.0
    progress_bar.numerator = 19
    assert ' 95% (19/20 B) [############ ] eta 00:01 \\' == str(progress_bar)

    eta._NOW = lambda: 1411868731.5
    progress_bar.numerator = 20
    assert '100% (20/20 B) [#############] eta 00:00 |' == str(progress_bar)
