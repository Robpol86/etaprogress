import pytest

from etaprogress import ETA


def test_empty():
    eta = ETA(50)
    assert eta.stalled() is True
    assert eta.done is False
    assert eta.eta_datetime is None
    assert eta.eta_seconds is None
    assert 0 == eta.numerator
    assert eta.rate is None


def test_error_denominator():
    with pytest.raises(ValueError) as e:
        ETA(0)
    assert 'denominator may not be zero.' == e.value.message

    with pytest.raises(ValueError) as e:
        ETA(-50)
    assert 'denominator must be positive/absolute.' == e.value.message


def test_error_numerator():
    eta = ETA(50)
    eta._now = lambda: 1411868722.680839
    eta.set_numerator(1)

    with pytest.raises(ValueError) as e:
        eta.set_numerator(0)
    assert 'cannot edit past numerators.' == e.value.message

    with pytest.raises(ValueError) as e:
        eta.set_numerator(2, 1311868700)
    assert 'timestamp may not decrement (slope must be positive).' == e.value.message

    with pytest.raises(ValueError) as e:
        eta.set_numerator(2, 1511868700)
    assert 'timestamp must not be in the future.' == e.value.message
