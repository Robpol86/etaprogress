from etaprogress import ETA


def test_linear_slope_1():
    eta = ETA(100)
    eta._timing_data = [(10, 10), (20, 20), (30, 30), (40, 40)]
    getattr(eta, '_calculate')()

    assert 100 == eta.eta_epoch
    assert 1.0 == eta.rate


def test_linear_slope_2():
    eta = ETA(100)
    eta._timing_data = [(10, 20), (20, 40), (30, 60), (40, 80)]
    getattr(eta, '_calculate')()

    assert 50 == eta.eta_epoch
    assert 2.0 == eta.rate


def test_cubic():
    """Wolfram Alpha:

    x is the timestamp. y is the numerator. 120 is the denominator.

    linear fit {1.2, 22},{2.4, 58},{3.1, 102},{4.4, 118}
    """
    return  # TODO
    eta = ETA(120)
    eta._timing_data = [
        (1411940269.184025, 22),
        (1411940269.753293, 58),
        (1411940270.323016, 102),
        (1411940270.891795, 118),
    ]
    getattr(eta, '_calculate')()

    assert 50 == eta.eta_epoch
    assert 2.0 == eta.rate




"""
TODO:

1) Swap axis. Since x is always time.time(), maybe go back to a list of tuples?
2) Eliminate custom timestamp in set_numerator(). _now() is already testable.
3) Add .started and .stalled properties for convenience.
4) Need those to mimic wget's moving <=> if not started.
5) I think wget detects stalled when slope is 0, do the same. Replace eta with stalled.
"""