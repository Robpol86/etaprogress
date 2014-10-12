import locale

import pytest

from etaprogress import eta, progress_components
from etaprogress.progress import ProgressBarBytes

LOCALES = (
    ('de_DE.UTF-8', '1023,96'),
    ('pt_BR.ISO8859-1', '1.023,96'),
    ('ru_RU.UTF-8', '1 023,96'),
)


@pytest.fixture(autouse=True, scope='module')
def define_locale(request):
    request.addfinalizer(lambda: locale.resetlocale())


@pytest.mark.parametrize('loc,val', LOCALES)
def test(loc, val):
    locale.setlocale(locale.LC_ALL, loc)
    progress_components.DEFAULT_TERMINAL_WIDTH = 50

    # Test undefined.
    progress_bar = ProgressBarBytes(None)
    assert '0 B [?                               ] eta --:-- /' == progress_bar.bar
    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(1073700000)
    expected = '{0} MiB [ ?                     '.format(val)
    assert progress_bar.bar.startswith(expected)

    # Test defined.
    progress_bar = ProgressBarBytes(1073700000)
    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(1073700000)
    expected = '100% ({0}/{0} MiB) [#######'.format(val)
    assert progress_bar.bar.startswith(expected)
