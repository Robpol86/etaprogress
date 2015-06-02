import locale
import os

import pytest


@pytest.fixture(autouse=True, scope='session')
def set_locale():
    if os.name == 'nt':
        locale.setlocale(locale.LC_ALL, 'english-us')
        return

    for l in ('en_US.utf8', 'english-us', 'english_us', 'en_us'):
        try:
            locale.setlocale(locale.LC_ALL, l)
        except locale.Error:
            continue
        return

    locale.resetlocale()
