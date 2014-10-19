from etaprogress.components.eta_conversions import eta_hms


def test():
    assert '00' == eta_hms(0)
    assert '09' == eta_hms(9)

    assert '59' == eta_hms(59)
    assert '01:00' == eta_hms(60)
    assert '01:01' == eta_hms(61)

    assert '59:59' == eta_hms(3599)
    assert '1:00:00' == eta_hms(3600)
    assert '1:00:01' == eta_hms(3601)
    assert '1:01:01' == eta_hms(3661)

    assert '167:59:59' == eta_hms(604799)
    assert '168:00:00' == eta_hms(604800)
    assert '168:00:01' == eta_hms(604801)


def test_always_show_minutes():
    assert '00:00' == eta_hms(0, always_show_minutes=True)
    assert '00:09' == eta_hms(9, always_show_minutes=True)

    assert '00:59' == eta_hms(59, always_show_minutes=True)
    assert '01:00' == eta_hms(60, always_show_minutes=True)
    assert '01:01' == eta_hms(61, always_show_minutes=True)

    assert '59:59' == eta_hms(3599, always_show_minutes=True)
    assert '1:00:00' == eta_hms(3600, always_show_minutes=True)
    assert '1:00:01' == eta_hms(3601, always_show_minutes=True)
    assert '1:01:01' == eta_hms(3661, always_show_minutes=True)

    assert '167:59:59' == eta_hms(604799, always_show_minutes=True)
    assert '168:00:00' == eta_hms(604800, always_show_minutes=True)
    assert '168:00:01' == eta_hms(604801, always_show_minutes=True)


def test_always_show_hours():
    assert '0:00:00' == eta_hms(0, always_show_hours=True)
    assert '0:00:09' == eta_hms(9, always_show_hours=True)

    assert '0:00:59' == eta_hms(59, always_show_hours=True)
    assert '0:01:00' == eta_hms(60, always_show_hours=True)
    assert '0:01:01' == eta_hms(61, always_show_hours=True)

    assert '0:59:59' == eta_hms(3599, always_show_hours=True)
    assert '1:00:00' == eta_hms(3600, always_show_hours=True)
    assert '1:00:01' == eta_hms(3601, always_show_hours=True)
    assert '1:01:01' == eta_hms(3661, always_show_hours=True)

    assert '167:59:59' == eta_hms(604799, always_show_hours=True)
    assert '168:00:00' == eta_hms(604800, always_show_hours=True)
    assert '168:00:01' == eta_hms(604801, always_show_hours=True)


####### The rest is mostly copy/pasted. ########


def test_hours_leading_zero():
    assert '00' == eta_hms(0, hours_leading_zero=True)
    assert '09' == eta_hms(9, hours_leading_zero=True)

    assert '59' == eta_hms(59, hours_leading_zero=True)
    assert '01:00' == eta_hms(60, hours_leading_zero=True)
    assert '01:01' == eta_hms(61, hours_leading_zero=True)

    assert '59:59' == eta_hms(3599, hours_leading_zero=True)
    assert '01:00:00' == eta_hms(3600, hours_leading_zero=True)
    assert '01:00:01' == eta_hms(3601, hours_leading_zero=True)
    assert '01:01:01' == eta_hms(3661, hours_leading_zero=True)

    assert '167:59:59' == eta_hms(604799, hours_leading_zero=True)
    assert '168:00:00' == eta_hms(604800, hours_leading_zero=True)
    assert '168:00:01' == eta_hms(604801, hours_leading_zero=True)


def test_always_show_minutes_hours_leading_zero():
    assert '00:00' == eta_hms(0, hours_leading_zero=True, always_show_minutes=True)
    assert '00:09' == eta_hms(9, hours_leading_zero=True, always_show_minutes=True)

    assert '00:59' == eta_hms(59, hours_leading_zero=True, always_show_minutes=True)
    assert '01:00' == eta_hms(60, hours_leading_zero=True, always_show_minutes=True)
    assert '01:01' == eta_hms(61, hours_leading_zero=True, always_show_minutes=True)

    assert '59:59' == eta_hms(3599, hours_leading_zero=True, always_show_minutes=True)
    assert '01:00:00' == eta_hms(3600, hours_leading_zero=True, always_show_minutes=True)
    assert '01:00:01' == eta_hms(3601, hours_leading_zero=True, always_show_minutes=True)
    assert '01:01:01' == eta_hms(3661, hours_leading_zero=True, always_show_minutes=True)

    assert '167:59:59' == eta_hms(604799, hours_leading_zero=True, always_show_minutes=True)
    assert '168:00:00' == eta_hms(604800, hours_leading_zero=True, always_show_minutes=True)
    assert '168:00:01' == eta_hms(604801, hours_leading_zero=True, always_show_minutes=True)


def test_always_show_hours_hours_leading_zero():
    assert '00:00:00' == eta_hms(0, hours_leading_zero=True, always_show_hours=True)
    assert '00:00:09' == eta_hms(9, hours_leading_zero=True, always_show_hours=True)

    assert '00:00:59' == eta_hms(59, hours_leading_zero=True, always_show_hours=True)
    assert '00:01:00' == eta_hms(60, hours_leading_zero=True, always_show_hours=True)
    assert '00:01:01' == eta_hms(61, hours_leading_zero=True, always_show_hours=True)

    assert '00:59:59' == eta_hms(3599, hours_leading_zero=True, always_show_hours=True)
    assert '01:00:00' == eta_hms(3600, hours_leading_zero=True, always_show_hours=True)
    assert '01:00:01' == eta_hms(3601, hours_leading_zero=True, always_show_hours=True)
    assert '01:01:01' == eta_hms(3661, hours_leading_zero=True, always_show_hours=True)

    assert '167:59:59' == eta_hms(604799, hours_leading_zero=True, always_show_hours=True)
    assert '168:00:00' == eta_hms(604800, hours_leading_zero=True, always_show_hours=True)
    assert '168:00:01' == eta_hms(604801, hours_leading_zero=True, always_show_hours=True)
