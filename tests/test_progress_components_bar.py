import pytest

from etaprogress.progress_components import Bar


def test_errors():
    bar = Bar()

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10)

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10, -1)

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10, 100.1)


def test_undefined_empty():
    bar = Bar(undefined_empty=True)

    assert '[        ]' == getattr(bar, '_bar')(10)
    assert '[        ]' == getattr(bar, '_bar')(10, 0.1)
    assert '[        ]' == getattr(bar, '_bar')(10, 100)


def test_undefined_animated():
    bar = Bar(undefined_animated=True)

    assert '[?       ]' == getattr(bar, '_bar')(10)
    assert '[ ?      ]' == getattr(bar, '_bar')(10, 0.1)
    assert '[  ?     ]' == getattr(bar, '_bar')(10, 100)

    assert '[   ?    ]' == getattr(bar, '_bar')(10)
    assert '[    ?   ]' == getattr(bar, '_bar')(10)
    assert '[     ?  ]' == getattr(bar, '_bar')(10)
    assert '[      ? ]' == getattr(bar, '_bar')(10)
    assert '[       ?]' == getattr(bar, '_bar')(10)
    assert '[      ? ]' == getattr(bar, '_bar')(10)
    assert '[     ?  ]' == getattr(bar, '_bar')(10)
    assert '[    ?   ]' == getattr(bar, '_bar')(10)
    assert '[   ?    ]' == getattr(bar, '_bar')(10)
    assert '[  ?     ]' == getattr(bar, '_bar')(10)
    assert '[ ?      ]' == getattr(bar, '_bar')(10)
    assert '[?       ]' == getattr(bar, '_bar')(10)
    assert '[ ?      ]' == getattr(bar, '_bar')(10)
    assert '[  ?     ]' == getattr(bar, '_bar')(10)


def test_undefined_animated_resize():
    bar = Bar(undefined_animated=True)

    assert '[?       ]' == getattr(bar, '_bar')(10)
    assert '[ ?      ]' == getattr(bar, '_bar')(10)
    assert '[  ?     ]' == getattr(bar, '_bar')(10)
    assert '[   ?    ]' == getattr(bar, '_bar')(10)
    assert '[    ?   ]' == getattr(bar, '_bar')(10)
    assert '[     ?  ]' == getattr(bar, '_bar')(10)
    assert '[ ? ]' == getattr(bar, '_bar')(5)
    assert '[?       ]' == getattr(bar, '_bar')(10)
    assert '[ ?      ]' == getattr(bar, '_bar')(10)


def test_undefined_animated_large():
    bar = Bar(undefined_animated=True)
    bar.CHARS_BAR_LEFT_BORDER = ' ['
    bar.CHARS_BAR_RIGHT_BORDER = '] '
    bar.CHARS_BAR_UNDEFINED_ANIMATED = '<?>'

    assert ' [<?>   ] ' == getattr(bar, '_bar')(10)
    assert ' [ <?>  ] ' == getattr(bar, '_bar')(10)
    assert ' [  <?> ] ' == getattr(bar, '_bar')(10)
    assert ' [   <?>] ' == getattr(bar, '_bar')(10)
    assert ' [  <?> ] ' == getattr(bar, '_bar')(10)
    assert ' [ <?>  ] ' == getattr(bar, '_bar')(10)
    assert ' [<?>   ] ' == getattr(bar, '_bar')(10)
    assert ' [ <?>  ] ' == getattr(bar, '_bar')(10)
    assert ' [  <?> ] ' == getattr(bar, '_bar')(10)


def test_defined_leading():
    bar = Bar(with_leading=True)
    bar.CHAR_BAR_UNIT_LEADING = '>'
    bar.CHAR_BAR_UNIT_FULL = '='
    bar.CHAR_BAR_UNIT_HALF = '-'

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10)

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10, -1)

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10, 100.1)

    assert '[          ]' == getattr(bar, '_bar')(12, 0)
    assert '[          ]' == getattr(bar, '_bar')(12, 9)
    assert '[>         ]' == getattr(bar, '_bar')(12, 10)
    assert '[>         ]' == getattr(bar, '_bar')(12, 15)
    assert '[=>        ]' == getattr(bar, '_bar')(12, 20)
    assert '[====>     ]' == getattr(bar, '_bar')(12, 50)
    assert '[========> ]' == getattr(bar, '_bar')(12, 99)
    assert '[=========>]' == getattr(bar, '_bar')(12, 100)


def test_defined_half_and_full():
    bar = Bar()
    bar.CHAR_BAR_UNIT_FULL = '='
    bar.CHAR_BAR_UNIT_HALF = '-'

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10)

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10, -1)

    with pytest.raises(ValueError):
        getattr(bar, '_bar')(10, 100.1)

    assert '[          ]' == getattr(bar, '_bar')(12, 0)
    assert '[-         ]' == getattr(bar, '_bar')(12, 9)
    assert '[=         ]' == getattr(bar, '_bar')(12, 10)
    assert '[=-        ]' == getattr(bar, '_bar')(12, 15)
    assert '[==        ]' == getattr(bar, '_bar')(12, 20)
    assert '[=====     ]' == getattr(bar, '_bar')(12, 50)
    assert '[=========-]' == getattr(bar, '_bar')(12, 99)
    assert '[==========]' == getattr(bar, '_bar')(12, 100)


def test_defined_full_only():
    bar = Bar()

    assert '[          ]' == getattr(bar, '_bar')(12, 0)
    assert '[          ]' == getattr(bar, '_bar')(12, 9)
    assert '[#         ]' == getattr(bar, '_bar')(12, 10)
    assert '[#         ]' == getattr(bar, '_bar')(12, 15)
    assert '[##        ]' == getattr(bar, '_bar')(12, 20)
    assert '[#####     ]' == getattr(bar, '_bar')(12, 50)
    assert '[######### ]' == getattr(bar, '_bar')(12, 99)
    assert '[##########]' == getattr(bar, '_bar')(12, 100)


def test_empty_char():
    bar = Bar()
    bar.CHAR_BAR_UNIT_HALF = '.'
    bar.CHAR_BAR_UNIT_EMPTY = '.'

    assert '[..........]' == getattr(bar, '_bar')(12, 0)
    assert '[..........]' == getattr(bar, '_bar')(12, 9)
    assert '[#.........]' == getattr(bar, '_bar')(12, 10)
    assert '[#.........]' == getattr(bar, '_bar')(12, 15)
    assert '[##........]' == getattr(bar, '_bar')(12, 20)
    assert '[#####.....]' == getattr(bar, '_bar')(12, 50)
    assert '[#########.]' == getattr(bar, '_bar')(12, 99)
    assert '[##########]' == getattr(bar, '_bar')(12, 100)
