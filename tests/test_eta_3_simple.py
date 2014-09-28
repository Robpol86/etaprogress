from etaprogress import ETA


def test_one():
    eta = ETA(1)
    eta._now = lambda: 1411868722.680839
    eta.set_numerator(1)

    assert 1 == eta.denominator
    assert eta.eta_epoch is None
    assert 0.0 == eta.rate
    assert eta.done is True
    assert eta.eta_datetime is None
    assert eta.eta_seconds is None
    assert 1 == eta.numerator
    assert eta.stalled is True
    assert eta.started is False


def test_two():
    eta = ETA(2)

    eta._now = lambda: 1411868721.680839
    eta.set_numerator(1)
    assert 2 == eta.denominator
    assert eta.eta_epoch is None
    assert 0.0 == eta.rate
    assert eta.done is False
    assert eta.eta_datetime is None
    assert eta.eta_seconds is None
    assert 1 == eta.numerator
    assert eta.stalled is True
    assert eta.started is False

    eta._now = lambda: 1411868722.680839
    eta.set_numerator(2)
    assert 2 == eta.denominator
    assert eta.done is True
    assert 2 == eta.numerator
