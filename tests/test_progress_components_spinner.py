from etaprogress.progress_components import Spinner


def test():
    spinner = Spinner()

    assert '/' == getattr(spinner, '_spinner')
    assert '-' == getattr(spinner, '_spinner')
    assert '\\' == getattr(spinner, '_spinner')
    assert '|' == getattr(spinner, '_spinner')
    assert '/' == getattr(spinner, '_spinner')
    assert '-' == getattr(spinner, '_spinner')
    assert '\\' == getattr(spinner, '_spinner')
    assert '|' == getattr(spinner, '_spinner')
