from etaprogress.progress_components import EtaLetters


def test():
    eta = EtaLetters()

    assert '0s' == getattr(eta, '_eta')(0)
    assert '9s' == getattr(eta, '_eta')(9)

    assert '59s' == getattr(eta, '_eta')(59)
    assert '1m' == getattr(eta, '_eta')(60)
    assert '1m 1s' == getattr(eta, '_eta')(61)

    assert '59m 59s' == getattr(eta, '_eta')(3599)
    assert '1h' == getattr(eta, '_eta')(3600)
    assert '1h 1s' == getattr(eta, '_eta')(3601)
    assert '1h 1m 1s' == getattr(eta, '_eta')(3661)

    assert '6d 23h 59m 59s' == getattr(eta, '_eta')(604799)
    assert '1w' == getattr(eta, '_eta')(604800)
    assert '1w 1s' == getattr(eta, '_eta')(604801)


def test_leading_zero():
    eta = EtaLetters(leading_zero=True)

    assert '00s' == getattr(eta, '_eta')(0)
    assert '09s' == getattr(eta, '_eta')(9)

    assert '59s' == getattr(eta, '_eta')(59)
    assert '01m' == getattr(eta, '_eta')(60)
    assert '01m 01s' == getattr(eta, '_eta')(61)

    assert '59m 59s' == getattr(eta, '_eta')(3599)
    assert '1h' == getattr(eta, '_eta')(3600)
    assert '1h 01s' == getattr(eta, '_eta')(3601)
    assert '1h 01m 01s' == getattr(eta, '_eta')(3661)

    assert '6d 23h 59m 59s' == getattr(eta, '_eta')(604799)
    assert '1w' == getattr(eta, '_eta')(604800)
    assert '1w 01s' == getattr(eta, '_eta')(604801)


def test_shortest():
    eta = EtaLetters(shortest=True)

    assert '0s' == getattr(eta, '_eta')(0)
    assert '9s' == getattr(eta, '_eta')(9)

    assert '59s' == getattr(eta, '_eta')(59)
    assert '1m' == getattr(eta, '_eta')(60)
    assert '1m' == getattr(eta, '_eta')(61)

    assert '59m' == getattr(eta, '_eta')(3599)
    assert '1h' == getattr(eta, '_eta')(3600)
    assert '1h' == getattr(eta, '_eta')(3601)
    assert '1h' == getattr(eta, '_eta')(3661)

    assert '6d' == getattr(eta, '_eta')(604799)
    assert '1w' == getattr(eta, '_eta')(604800)
    assert '1w' == getattr(eta, '_eta')(604801)


def test_shortest_and_leading_zero():
    eta = EtaLetters(shortest=True, leading_zero=True)

    assert '00s' == getattr(eta, '_eta')(0)
    assert '09s' == getattr(eta, '_eta')(9)

    assert '59s' == getattr(eta, '_eta')(59)
    assert '01m' == getattr(eta, '_eta')(60)
    assert '01m' == getattr(eta, '_eta')(61)

    assert '59m' == getattr(eta, '_eta')(3599)
    assert '1h' == getattr(eta, '_eta')(3600)
    assert '1h' == getattr(eta, '_eta')(3601)
    assert '1h' == getattr(eta, '_eta')(3661)

    assert '6d' == getattr(eta, '_eta')(604799)
    assert '1w' == getattr(eta, '_eta')(604800)
    assert '1w' == getattr(eta, '_eta')(604801)
