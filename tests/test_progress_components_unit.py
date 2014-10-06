import pytest

from etaprogress.progress_components import Unit


def test_errors():
    with pytest.raises(ValueError):
        Unit(non_rate_unit='dne')

    with pytest.raises(ValueError):
        Unit(rate_unit='dne')

    unit = Unit(non_rate_unit='bytes', rate_unit='bytes')
    getattr(unit, '_Unit__unit')(524288, unit='MiB')
    getattr(unit, '_Unit__unit')(524288, rate=True, unit='MiB/s')
    with pytest.raises(IndexError):
        getattr(unit, '_Unit__unit')(524288, unit='MiB/s')
    with pytest.raises(IndexError):
        getattr(unit, '_Unit__unit')(524288, rate=True, unit='MiB')


def test_default():
    unit = Unit()
    assert (0, '', '/s') == getattr(unit, '_Unit__unit')(0)
    assert (0, '', '/s') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, '', '/s') == getattr(unit, '_Unit__unit')(1)
    assert (1, '', '/s') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1000, '', '/s') == getattr(unit, '_Unit__unit')(1000)
    assert (1000, '', '/s') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000)
    assert (1000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bits_one():
    unit = Unit(non_rate_unit='bits')
    assert (0, 'b', 'bps') == getattr(unit, '_Unit__unit')(0)
    assert (0, '', '/s') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, 'b', 'bps') == getattr(unit, '_Unit__unit')(1)
    assert (1, '', '/s') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1, 'kb', 'kbps') == getattr(unit, '_Unit__unit')(1000)
    assert (1000, '', '/s') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1, 'mb', 'mbps') == getattr(unit, '_Unit__unit')(1000000)
    assert (1000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1, 'gb', 'gbps') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bits_two():
    unit = Unit(rate_unit='bits')
    assert (0, '', '/s') == getattr(unit, '_Unit__unit')(0)
    assert (0, 'b', 'bps') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, '', '/s') == getattr(unit, '_Unit__unit')(1)
    assert (1, 'b', 'bps') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1000, '', '/s') == getattr(unit, '_Unit__unit')(1000)
    assert (1, 'kb', 'kbps') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000)
    assert (1, 'mb', 'mbps') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1, 'gb', 'gbps') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000000000000000, '', '/s') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bits_three():
    unit = Unit(non_rate_unit='bits', rate_unit='bits')
    assert (0, 'b', 'bps') == getattr(unit, '_Unit__unit')(0)
    assert (0, 'b', 'bps') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, 'b', 'bps') == getattr(unit, '_Unit__unit')(1)
    assert (1, 'b', 'bps') == getattr(unit, '_Unit__unit')(1, rate=True)
    assert (1, 'kb', 'kbps') == getattr(unit, '_Unit__unit')(1000)
    assert (1, 'kb', 'kbps') == getattr(unit, '_Unit__unit')(1000, rate=True)
    assert (1, 'mb', 'mbps') == getattr(unit, '_Unit__unit')(1000000)
    assert (1, 'mb', 'mbps') == getattr(unit, '_Unit__unit')(1000000, rate=True)
    assert (1, 'gb', 'gbps') == getattr(unit, '_Unit__unit')(1000000000)
    assert (1, 'gb', 'gbps') == getattr(unit, '_Unit__unit')(1000000000, rate=True)
    assert (1, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000)
    assert (1, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000, rate=True)
    assert (1000, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000000)
    assert (1000, 'tb', 'tbps') == getattr(unit, '_Unit__unit')(1000000000000000, rate=True)


def test_bytes():
    unit = Unit(non_rate_unit='bytes', rate_unit='bytes')
    assert (0, 'B', 'B/s') == getattr(unit, '_Unit__unit')(0)
    assert (0, 'B', 'B/s') == getattr(unit, '_Unit__unit')(0, rate=True)
    assert (1, 'B', 'B/s') == getattr(unit, '_Unit__unit')(1)
    assert (1, 'B', 'B/s') == getattr(unit, '_Unit__unit')(1, rate=True)

    assert (1, 'KiB', 'KiB/s') == getattr(unit, '_Unit__unit')(1024)
    assert (1, 'KiB', 'KiB/s') == getattr(unit, '_Unit__unit')(1024, rate=True)
    assert (1.25, 'KiB', 'KiB/s') == getattr(unit, '_Unit__unit')(1280)
    assert (1.25, 'KiB', 'KiB/s') == getattr(unit, '_Unit__unit')(1280, rate=True)

    assert (512, 'KiB', 'KiB/s') == getattr(unit, '_Unit__unit')(524288)
    assert (512, 'KiB', 'KiB/s') == getattr(unit, '_Unit__unit')(524288, rate=True)
    assert (0.5, 'MiB', 'MiB/s') == getattr(unit, '_Unit__unit')(524288, unit='MiB')
    assert (0.5, 'MiB', 'MiB/s') == getattr(unit, '_Unit__unit')(524288, rate=True, unit='MiB/s')

    assert (1, 'MiB', 'MiB/s') == getattr(unit, '_Unit__unit')(1048576)
    assert (1, 'MiB', 'MiB/s') == getattr(unit, '_Unit__unit')(1048576, rate=True)

    assert (1, 'GiB', 'GiB/s') == getattr(unit, '_Unit__unit')(1073741824)
    assert (1, 'GiB', 'GiB/s') == getattr(unit, '_Unit__unit')(1073741824, rate=True)

    assert (1, 'TiB', 'TiB/s') == getattr(unit, '_Unit__unit')(1099511627776)
    assert (1, 'TiB', 'TiB/s') == getattr(unit, '_Unit__unit')(1099511627776, rate=True)

    assert (1000, 'TiB', 'TiB/s') == getattr(unit, '_Unit__unit')(1099511627776000)
    assert (1000, 'TiB', 'TiB/s') == getattr(unit, '_Unit__unit')(1099511627776000, rate=True)
