import locale
import os

import pytest


@pytest.fixture(autouse=True, scope='session')
def set_locale():
    if os.name == 'nt':
        locale.setlocale(locale.LC_ALL, 'english-us')
    else:
        locale.resetlocale()
