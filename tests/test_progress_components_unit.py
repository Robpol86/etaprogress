import pytest

from etaprogress.progress_components import Unit


def test_errors():
    with pytest.raises(ValueError):
        Unit(**dict(_Unit__non_rate_unit='dne'))

    with pytest.raises(ValueError):
        Unit(**dict(_Unit__rate_unit='dne'))


def test_default():
    unit = Unit()
    assert (0, '') == getattr(unit, '_Unit__unit')(0)
    assert (0, '/s') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, '') == getattr(unit, '_Unit__unit')(1)
    assert (1, '/s') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1000, '') == getattr(unit, '_Unit__unit')(1000)
    assert (1000, '/s') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1000000, '') == getattr(unit, '_Unit__unit')(1000000)
    assert (1000000, '/s') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1000000000, '') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1000000000, '/s') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1000000000000, '') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1000000000000, '/s') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000000000000000, '') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000000000000000, '/s') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bits_one():
    unit = Unit(**dict(_Unit__non_rate_unit='bits'))
    assert (0, 'b') == getattr(unit, '_Unit__unit')(0)
    assert (0, '/s') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, 'b') == getattr(unit, '_Unit__unit')(1)
    assert (1, '/s') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1, 'kb') == getattr(unit, '_Unit__unit')(1000)
    assert (1000, '/s') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1, 'mb') == getattr(unit, '_Unit__unit')(1000000)
    assert (1000000, '/s') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1, 'gb') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1000000000, '/s') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1, 'tb') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1000000000000, '/s') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000, 'tb') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000000000000000, '/s') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bits_two():
    unit = Unit(**dict(_Unit__rate_unit='bits'))
    assert (0, '') == getattr(unit, '_Unit__unit')(0)
    assert (0, 'bps') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, '') == getattr(unit, '_Unit__unit')(1)
    assert (1, 'bps') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1000, '') == getattr(unit, '_Unit__unit')(1000)
    assert (1, 'kbps') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1000000, '') == getattr(unit, '_Unit__unit')(1000000)
    assert (1, 'mbps') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1000000000, '') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1, 'gbps') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1000000000000, '') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1, 'tbps') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000000000000000, '') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000, 'tbps') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bits_three():
    unit = Unit(**dict(_Unit__non_rate_unit='bits', _Unit__rate_unit='bits'))
    assert (0, 'b') == getattr(unit, '_Unit__unit')(0)
    assert (0, 'bps') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, 'b') == getattr(unit, '_Unit__unit')(1)
    assert (1, 'bps') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1, 'kb') == getattr(unit, '_Unit__unit')(1000)
    assert (1, 'kbps') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1, 'mb') == getattr(unit, '_Unit__unit')(1000000)
    assert (1, 'mbps') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1, 'gb') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1, 'gbps') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1, 'tb') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1, 'tbps') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000, 'tb') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000, 'tbps') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bytes():
    unit = Unit(**dict(_Unit__non_rate_unit='bytes', _Unit__rate_unit='bytes'))
    assert (0, 'B') == getattr(unit, '_Unit__unit')(0)
    assert (0, 'B/s') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, 'B') == getattr(unit, '_Unit__unit')(1)
    assert (1, 'B/s') == getattr(unit, '_Unit__unit')(1, rate=True)

    assert (1, 'KiB') == getattr(unit, '_Unit__unit')(1024)
    assert (1, 'KiB/s') == getattr(unit, '_Unit__unit')(1024, rate=True)
    assert (1.25, 'KiB') == getattr(unit, '_Unit__unit')(1280)
    assert (1.25, 'KiB/s') == getattr(unit, '_Unit__unit')(1280, rate=True)

    assert (1, 'MiB') == getattr(unit, '_Unit__unit')(1048576)
    assert (1, 'MiB/s') == getattr(unit, '_Unit__unit')(1048576, rate=True)

    assert (1, 'GiB') == getattr(unit, '_Unit__unit')(1073741824)
    assert (1, 'GiB/s') == getattr(unit, '_Unit__unit')(1073741824, rate=True)

    assert (1, 'TiB') == getattr(unit, '_Unit__unit')(1099511627776)
    assert (1, 'TiB/s') == getattr(unit, '_Unit__unit')(1099511627776, rate=True)

    assert (1000, 'TiB') == getattr(unit, '_Unit__unit')(1099511627776000)
    assert (1000, 'TiB/s') == getattr(unit, '_Unit__unit')(1099511627776000, rate=True)
