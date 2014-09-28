import pytest

from etaprogress import ETA


def test_empty():
    eta = ETA(50)
    assert 50 == eta.denominator
    assert eta.eta_epoch is None
    assert 0.0 == eta.rate
    assert eta.done is False
    assert eta.eta_datetime is None
    assert eta.eta_seconds is None
    assert 0 == eta.numerator
    assert eta.stalled is True
    assert eta.started is False


def test_error_denominator():
    with pytest.raises(ValueError) as e:
        ETA(0)
    assert 'denominator may not be zero.' == str(e.value)

    with pytest.raises(ValueError) as e:
        ETA(-50)
    assert 'denominator must be positive/absolute.' == str(e.value)


def test_error_numerator():
    eta = ETA(50)
    eta._now = lambda: 1411868722.680839
    eta.set_numerator(1)

    with pytest.raises(ValueError) as e:
        eta.set_numerator(0)
    assert 'numerator cannot decrement.' == str(e.value)
