from etaprogress.components.bars import Bar, BarDoubled


def test_bar():
    bar = Bar()

    assert '[          ]' == bar.bar(12, 0)
    assert '[          ]' == bar.bar(12, 9)
    assert '[#         ]' == bar.bar(12, 10)
    assert '[#         ]' == bar.bar(12, 15)
    assert '[##        ]' == bar.bar(12, 20)
    assert '[#####     ]' == bar.bar(12, 50)
    assert '[######### ]' == bar.bar(12, 99)
    assert '[##########]' == bar.bar(12, 100)


def test_bar_leading_empty_char(request):
    def fin():
        Bar.CHAR_EMPTY = ' '
        Bar.CHAR_FULL = '#'
        Bar.CHAR_LEADING = '#'
    request.addfinalizer(fin)

    Bar.CHAR_EMPTY = '.'
    Bar.CHAR_FULL = '='
    Bar.CHAR_LEADING = '>'
    bar = Bar()

    assert '[..........]' == bar.bar(12, 0)
    assert '[..........]' == bar.bar(12, 9)
    assert '[>.........]' == bar.bar(12, 10)
    assert '[>.........]' == bar.bar(12, 15)
    assert '[=>........]' == bar.bar(12, 20)
    assert '[====>.....]' == bar.bar(12, 50)
    assert '[========>.]' == bar.bar(12, 99)
    assert '[=========>]' == bar.bar(12, 100)


def test_bar_doubled():
    bar = BarDoubled()

    assert '[          ]' == bar.bar(12, 0)
    assert '[-         ]' == bar.bar(12, 9)
    assert '[=         ]' == bar.bar(12, 10)
    assert '[=-        ]' == bar.bar(12, 15)
    assert '[==        ]' == bar.bar(12, 20)
    assert '[=====     ]' == bar.bar(12, 50)
    assert '[=========-]' == bar.bar(12, 99)
    assert '[==========]' == bar.bar(12, 100)
