from etaprogress import progress_components
from etaprogress.progress import ProgressBar


def test_undefined():
    progress_components.DEFAULT_TERMINAL_WIDTH = 30
    progress_bar = ProgressBar(None)

    assert '0 [?             ] eta --:-- /' == progress_bar.bar
    assert '0 [ ?            ] eta --:-- -' == progress_bar.bar
    assert '0 [  ?           ] eta --:-- \\' == progress_bar.bar
