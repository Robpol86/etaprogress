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


def test_linear_transform():
    """Wolfram Alpha:
    x is the timestamp. y is the numerator. 120 is the denominator.
    linear fit {1.2, 22},{2.4, 58},{3.1, 102},{4.4, 118}

    The closer we get to 100%, the more vertical shift/transform is applied to the line.
    As we near the end we want the line to get closer to the last point on the graph.
    This avoids having 99% with an ETA in the past.
    """
    eta = ETA(120)
    eta._timing_data = [(1.2, 22), (2.4, 58), (3.1, 102), (4.4, 118)]
    getattr(eta, '_calculate')()

    assert 4.4 < eta.eta_epoch < 4.6
    assert 30 < eta.rate < 35

