from etaprogress.components.eta_conversions import eta_letters


def test():
    assert '0s' == eta_letters(0)
    assert '9s' == eta_letters(9)

    assert '59s' == eta_letters(59)
    assert '1m' == eta_letters(60)
    assert '1m 1s' == eta_letters(61)

    assert '59m 59s' == eta_letters(3599)
    assert '1h' == eta_letters(3600)
    assert '1h 1s' == eta_letters(3601)
    assert '1h 1m 1s' == eta_letters(3661)

    assert '6d 23h 59m 59s' == eta_letters(604799)
    assert '1w' == eta_letters(604800)
    assert '1w 1s' == eta_letters(604801)


def test_leading_zero():
    assert '00s' == eta_letters(0, leading_zero=True)
    assert '09s' == eta_letters(9, leading_zero=True)

    assert '59s' == eta_letters(59, leading_zero=True)
    assert '01m' == eta_letters(60, leading_zero=True)
    assert '01m 01s' == eta_letters(61, leading_zero=True)

    assert '59m 59s' == eta_letters(3599, leading_zero=True)
    assert '1h' == eta_letters(3600, leading_zero=True)
    assert '1h 01s' == eta_letters(3601, leading_zero=True)
    assert '1h 01m 01s' == eta_letters(3661, leading_zero=True)

    assert '6d 23h 59m 59s' == eta_letters(604799, leading_zero=True)
    assert '1w' == eta_letters(604800, leading_zero=True)
    assert '1w 01s' == eta_letters(604801, leading_zero=True)


def test_shortest():
    assert '0s' == eta_letters(0, shortest=True)
    assert '9s' == eta_letters(9, shortest=True)

    assert '59s' == eta_letters(59, shortest=True)
    assert '1m' == eta_letters(60, shortest=True)
    assert '1m' == eta_letters(61, shortest=True)

    assert '59m' == eta_letters(3599, shortest=True)
    assert '1h' == eta_letters(3600, shortest=True)
    assert '1h' == eta_letters(3601, shortest=True)
    assert '1h' == eta_letters(3661, shortest=True)

    assert '6d' == eta_letters(604799, shortest=True)
    assert '1w' == eta_letters(604800, shortest=True)
    assert '1w' == eta_letters(604801, shortest=True)


def test_shortest_and_leading_zero():
    assert '00s' == eta_letters(0, shortest=True, leading_zero=True)
    assert '09s' == eta_letters(9, shortest=True, leading_zero=True)

    assert '59s' == eta_letters(59, shortest=True, leading_zero=True)
    assert '01m' == eta_letters(60, shortest=True, leading_zero=True)
    assert '01m' == eta_letters(61, shortest=True, leading_zero=True)

    assert '59m' == eta_letters(3599, shortest=True, leading_zero=True)
    assert '1h' == eta_letters(3600, shortest=True, leading_zero=True)
    assert '1h' == eta_letters(3601, shortest=True, leading_zero=True)
    assert '1h' == eta_letters(3661, shortest=True, leading_zero=True)

    assert '6d' == eta_letters(604799, shortest=True, leading_zero=True)
    assert '1w' == eta_letters(604800, shortest=True, leading_zero=True)
    assert '1w' == eta_letters(604801, shortest=True, leading_zero=True)
