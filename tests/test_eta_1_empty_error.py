import pytest

from etaprogress import eta


def test_empty():
    eta_instance = eta.ETA(50)
    assert 50 == eta_instance.denominator
    assert eta_instance.eta_epoch is None
    assert 0.0 == eta_instance.rate
    assert 0 == eta_instance.numerator
    assert eta_instance.stalled is True
    assert eta_instance.started is False
    assert eta_instance.undefined is False
    assert eta_instance.done is False
    assert eta_instance.eta_seconds is None
    assert 0.0 == eta_instance.percent
    assert 0.0 == eta_instance.elapsed
    assert 0.0 == eta_instance.rate_unstable
    assert 0.0 == eta_instance.rate_overall


def test_empty_undefined():
    eta_instance = eta.ETA(0)
    assert 0 == eta_instance.denominator
    assert eta_instance.eta_epoch is None
    assert 0.0 == eta_instance.rate
    assert 0 == eta_instance.numerator
    assert eta_instance.stalled is True
    assert eta_instance.started is False
    assert eta_instance.undefined is True
    assert eta_instance.done is False
    assert eta_instance.eta_seconds is None
    assert 0.0 == eta_instance.percent
    assert 0.0 == eta_instance.elapsed
    assert 0.0 == eta_instance.rate_unstable
    assert 0.0 == eta_instance.rate_overall

    eta_instance = eta.ETA(None)
    assert eta_instance.denominator is None
    assert eta_instance.eta_epoch is None
    assert 0.0 == eta_instance.rate
    assert 0 == eta_instance.numerator
    assert eta_instance.stalled is True
    assert eta_instance.started is False
    assert eta_instance.undefined is True
    assert eta_instance.done is False
    assert eta_instance.eta_seconds is None
    assert 0.0 == eta_instance.percent
    assert 0.0 == eta_instance.elapsed
    assert 0.0 == eta_instance.rate_unstable
    assert 0.0 == eta_instance.rate_overall


def test_error_numerator():
    eta_instance = eta.ETA(50)
    eta._NOW = lambda: 1411868722.680839
    eta_instance.set_numerator(1)

    with pytest.raises(ValueError) as e:
        eta_instance.set_numerator(0)
    assert 'numerator cannot decrement.' == str(e.value)
