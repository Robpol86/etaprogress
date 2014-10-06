import locale

from etaprogress import eta, progress_components
from etaprogress.progress import ProgressBar


def test_undefined():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    progress_components.DEFAULT_TERMINAL_WIDTH = 30
    progress_bar = ProgressBar(None)

    assert '0 [?             ] eta --:-- /' == progress_bar.bar
    assert '0 [ ?            ] eta --:-- -' == progress_bar.bar
    assert '0 [  ?           ] eta --:-- \\' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(10)
    assert '10 [   ?         ] eta --:-- |' == progress_bar.bar
    assert '10 [    ?        ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(100)
    assert '100 [     ?      ] eta --:-- -' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(1954727)
    assert '1,954,727 [    ? ] eta --:-- \\' == progress_bar.bar
    assert '1,954,727 [   ?  ] eta --:-- |' == progress_bar.bar


def test_defined():
    progress_components.DEFAULT_TERMINAL_WIDTH = 40
    progress_bar = ProgressBar(20)

    assert '  0% ( 0/20) [             ] eta --:-- /' == progress_bar.bar
    assert '  0% ( 0/20) [             ] eta --:-- -' == progress_bar.bar
    assert '  0% ( 0/20) [             ] eta --:-- \\' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert '  5% ( 1/20) [             ] eta --:-- |' == progress_bar.bar
    assert '  5% ( 1/20) [             ] eta --:-- /' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(2)
    assert ' 10% ( 2/20) [#            ] eta 00:09 -' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(3)
    assert ' 15% ( 3/20) [#            ] eta 00:08 \\' == progress_bar.bar
