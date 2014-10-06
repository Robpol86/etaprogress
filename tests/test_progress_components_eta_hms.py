from etaprogress.progress_components import EtaHMS


def test():
    eta = EtaHMS()

    assert '00' == getattr(eta, '_EtaHMS__eta')(0)
    assert '09' == getattr(eta, '_EtaHMS__eta')(9)

    assert '59' == getattr(eta, '_EtaHMS__eta')(59)
    assert '01:00' == getattr(eta, '_EtaHMS__eta')(60)
    assert '01:01' == getattr(eta, '_EtaHMS__eta')(61)

    assert '59:59' == getattr(eta, '_EtaHMS__eta')(3599)
    assert '1:00:00' == getattr(eta, '_EtaHMS__eta')(3600)
    assert '1:00:01' == getattr(eta, '_EtaHMS__eta')(3601)
    assert '1:01:01' == getattr(eta, '_EtaHMS__eta')(3661)

    assert '167:59:59' == getattr(eta, '_EtaHMS__eta')(604799)
    assert '168:00:00' == getattr(eta, '_EtaHMS__eta')(604800)
    assert '168:00:01' == getattr(eta, '_EtaHMS__eta')(604801)


def test_always_show_minutes():
    eta = EtaHMS(always_show_minutes=True)

    assert '00:00' == getattr(eta, '_EtaHMS__eta')(0)
    assert '00:09' == getattr(eta, '_EtaHMS__eta')(9)

    assert '00:59' == getattr(eta, '_EtaHMS__eta')(59)
    assert '01:00' == getattr(eta, '_EtaHMS__eta')(60)
    assert '01:01' == getattr(eta, '_EtaHMS__eta')(61)

    assert '59:59' == getattr(eta, '_EtaHMS__eta')(3599)
    assert '1:00:00' == getattr(eta, '_EtaHMS__eta')(3600)
    assert '1:00:01' == getattr(eta, '_EtaHMS__eta')(3601)
    assert '1:01:01' == getattr(eta, '_EtaHMS__eta')(3661)

    assert '167:59:59' == getattr(eta, '_EtaHMS__eta')(604799)
    assert '168:00:00' == getattr(eta, '_EtaHMS__eta')(604800)
    assert '168:00:01' == getattr(eta, '_EtaHMS__eta')(604801)


def test_always_show_hours():
    eta = EtaHMS(always_show_hours=True)

    assert '0:00:00' == getattr(eta, '_EtaHMS__eta')(0)
    assert '0:00:09' == getattr(eta, '_EtaHMS__eta')(9)

    assert '0:00:59' == getattr(eta, '_EtaHMS__eta')(59)
    assert '0:01:00' == getattr(eta, '_EtaHMS__eta')(60)
    assert '0:01:01' == getattr(eta, '_EtaHMS__eta')(61)

    assert '0:59:59' == getattr(eta, '_EtaHMS__eta')(3599)
    assert '1:00:00' == getattr(eta, '_EtaHMS__eta')(3600)
    assert '1:00:01' == getattr(eta, '_EtaHMS__eta')(3601)
    assert '1:01:01' == getattr(eta, '_EtaHMS__eta')(3661)

    assert '167:59:59' == getattr(eta, '_EtaHMS__eta')(604799)
    assert '168:00:00' == getattr(eta, '_EtaHMS__eta')(604800)
    assert '168:00:01' == getattr(eta, '_EtaHMS__eta')(604801)


####### The rest is mostly copy/pasted. ########


def test_hours_leading_zero():
    eta = EtaHMS(hours_leading_zero=True)

    assert '00' == getattr(eta, '_EtaHMS__eta')(0)
    assert '09' == getattr(eta, '_EtaHMS__eta')(9)

    assert '59' == getattr(eta, '_EtaHMS__eta')(59)
    assert '01:00' == getattr(eta, '_EtaHMS__eta')(60)
    assert '01:01' == getattr(eta, '_EtaHMS__eta')(61)

    assert '59:59' == getattr(eta, '_EtaHMS__eta')(3599)
    assert '01:00:00' == getattr(eta, '_EtaHMS__eta')(3600)
    assert '01:00:01' == getattr(eta, '_EtaHMS__eta')(3601)
    assert '01:01:01' == getattr(eta, '_EtaHMS__eta')(3661)

    assert '167:59:59' == getattr(eta, '_EtaHMS__eta')(604799)
    assert '168:00:00' == getattr(eta, '_EtaHMS__eta')(604800)
    assert '168:00:01' == getattr(eta, '_EtaHMS__eta')(604801)


def test_always_show_minutes_hours_leading_zero():
    eta = EtaHMS(hours_leading_zero=True, always_show_minutes=True)

    assert '00:00' == getattr(eta, '_EtaHMS__eta')(0)
    assert '00:09' == getattr(eta, '_EtaHMS__eta')(9)

    assert '00:59' == getattr(eta, '_EtaHMS__eta')(59)
    assert '01:00' == getattr(eta, '_EtaHMS__eta')(60)
    assert '01:01' == getattr(eta, '_EtaHMS__eta')(61)

    assert '59:59' == getattr(eta, '_EtaHMS__eta')(3599)
    assert '01:00:00' == getattr(eta, '_EtaHMS__eta')(3600)
    assert '01:00:01' == getattr(eta, '_EtaHMS__eta')(3601)
    assert '01:01:01' == getattr(eta, '_EtaHMS__eta')(3661)

    assert '167:59:59' == getattr(eta, '_EtaHMS__eta')(604799)
    assert '168:00:00' == getattr(eta, '_EtaHMS__eta')(604800)
    assert '168:00:01' == getattr(eta, '_EtaHMS__eta')(604801)


def test_always_show_hours_hours_leading_zero():
    eta = EtaHMS(hours_leading_zero=True, always_show_hours=True)

    assert '00:00:00' == getattr(eta, '_EtaHMS__eta')(0)
    assert '00:00:09' == getattr(eta, '_EtaHMS__eta')(9)

    assert '00:00:59' == getattr(eta, '_EtaHMS__eta')(59)
    assert '00:01:00' == getattr(eta, '_EtaHMS__eta')(60)
    assert '00:01:01' == getattr(eta, '_EtaHMS__eta')(61)

    assert '00:59:59' == getattr(eta, '_EtaHMS__eta')(3599)
    assert '01:00:00' == getattr(eta, '_EtaHMS__eta')(3600)
    assert '01:00:01' == getattr(eta, '_EtaHMS__eta')(3601)
    assert '01:01:01' == getattr(eta, '_EtaHMS__eta')(3661)

    assert '167:59:59' == getattr(eta, '_EtaHMS__eta')(604799)
    assert '168:00:00' == getattr(eta, '_EtaHMS__eta')(604800)
    assert '168:00:01' == getattr(eta, '_EtaHMS__eta')(604801)
