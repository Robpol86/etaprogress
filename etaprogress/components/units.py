"""Holds classes for handling unit conversions."""


class UnitBit(object):
    """Converts bits into other units such as kilobits, megabits, etc."""

    def __init__(self, value):
        self._value = value

    @property
    def b(self):
        """bit"""
        return self._value

    @property
    def kb(self):
        """kilobit"""
        return self._value / 1000.0

    @property
    def mb(self):
        """megabit"""
        return self._value / 1000000.0

    @property
    def gb(self):
        """gigabit"""
        return self._value / 1000000000.0

    @property
    def tb(self):
        """terabit"""
        return self._value / 1000000000000.0

    @property
    def auto(self):
        """Returns the highest whole-number unit."""
        if self._value >= 1000000000000:
            return self.tb, 'tb'
        if self._value >= 1000000000:
            return self.gb, 'gb'
        if self._value >= 1000000:
            return self.mb, 'mb'
        if self._value >= 1000:
            return self.kb, 'kb'
        else:
            return self.b, 'b'


class UnitByte(object):
    """Converts bytes into other units such as kibibytes (like kilobytes, 1 * 1024)."""

    def __init__(self, value):
        self._value = value

    @property
    def B(self):
        """byte"""
        return self._value

    @property
    def KiB(self):
        """kibibyte"""
        return self._value / 1024.0

    @property
    def MiB(self):
        """mebibyte"""
        return self._value / 1048576.0

    @property
    def GiB(self):
        """gibibyte"""
        return self._value / 1073741824.0

    @property
    def TiB(self):
        """tebibyte"""
        return self._value / 1099511627776.0

    @property
    def auto(self):
        """Returns the highest whole-number unit."""
        if self._value >= 1099511627776:
            return self.TiB, 'TiB'
        if self._value >= 1073741824:
            return self.GiB, 'GiB'
        if self._value >= 1048576:
            return self.MiB, 'MiB'
        if self._value >= 1024:
            return self.KiB, 'KiB'
        else:
            return self.B, 'B'

    @property
    def auto_no_thousands(self):
        """Like self.auto but calculates the next unit if >999.99."""
        if self._value >= 1000000000000:
            return self.TiB, 'TiB'
        if self._value >= 1000000000:
            return self.GiB, 'GiB'
        if self._value >= 1000000:
            return self.MiB, 'MiB'
        if self._value >= 1000:
            return self.KiB, 'KiB'
        else:
            return self.B, 'B'
