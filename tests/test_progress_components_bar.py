import pytest

from etaprogress.progress_components import Bar


def test_errors():
    bar = Bar()

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10)

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10, -1)

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10, 100.1)


def test_undefined_empty():
    bar = Bar(**dict(_Bar__undefined_empty=True))

    assert '[        ]' == getattr(bar, '_Bar__bar')(10)
    assert '[        ]' == getattr(bar, '_Bar__bar')(10, 0.1)
    assert '[        ]' == getattr(bar, '_Bar__bar')(10, 100)


def test_undefined_animated():
    bar = Bar(**dict(_Bar__undefined_animated=True))

    assert '[?       ]' == getattr(bar, '_Bar__bar')(10)
    assert '[ ?      ]' == getattr(bar, '_Bar__bar')(10, 0.1)
    assert '[  ?     ]' == getattr(bar, '_Bar__bar')(10, 100)

    assert '[   ?    ]' == getattr(bar, '_Bar__bar')(10)
    assert '[    ?   ]' == getattr(bar, '_Bar__bar')(10)
    assert '[     ?  ]' == getattr(bar, '_Bar__bar')(10)
    assert '[      ? ]' == getattr(bar, '_Bar__bar')(10)
    assert '[       ?]' == getattr(bar, '_Bar__bar')(10)
    assert '[      ? ]' == getattr(bar, '_Bar__bar')(10)
    assert '[     ?  ]' == getattr(bar, '_Bar__bar')(10)
    assert '[    ?   ]' == getattr(bar, '_Bar__bar')(10)
    assert '[   ?    ]' == getattr(bar, '_Bar__bar')(10)
    assert '[  ?     ]' == getattr(bar, '_Bar__bar')(10)
    assert '[ ?      ]' == getattr(bar, '_Bar__bar')(10)
    assert '[?       ]' == getattr(bar, '_Bar__bar')(10)
    assert '[ ?      ]' == getattr(bar, '_Bar__bar')(10)
    assert '[  ?     ]' == getattr(bar, '_Bar__bar')(10)


def test_undefined_animated_resize():
    bar = Bar(**dict(_Bar__undefined_animated=True))

    assert '[?       ]' == getattr(bar, '_Bar__bar')(10)
    assert '[ ?      ]' == getattr(bar, '_Bar__bar')(10)
    assert '[  ?     ]' == getattr(bar, '_Bar__bar')(10)
    assert '[   ?    ]' == getattr(bar, '_Bar__bar')(10)
    assert '[    ?   ]' == getattr(bar, '_Bar__bar')(10)
    assert '[     ?  ]' == getattr(bar, '_Bar__bar')(10)
    assert '[ ? ]' == getattr(bar, '_Bar__bar')(5)
    assert '[?       ]' == getattr(bar, '_Bar__bar')(10)
    assert '[ ?      ]' == getattr(bar, '_Bar__bar')(10)


def test_undefined_animated_large():
    bar = Bar(**dict(_Bar__undefined_animated=True))
    bar._Bar__CHARS_LEFT_BORDER = ' ['
    bar._Bar__CHARS_RIGHT_BORDER = '] '
    bar._Bar__CHARS_UNDEFINED_ANIMATED = '<?>'

    assert ' [<?>   ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [ <?>  ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [  <?> ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [   <?>] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [  <?> ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [ <?>  ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [<?>   ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [ <?>  ] ' == getattr(bar, '_Bar__bar')(10)
    assert ' [  <?> ] ' == getattr(bar, '_Bar__bar')(10)


def test_defined_leading():
    bar = Bar(**dict(_Bar__with_leading=True))
    bar._Bar__CHAR_UNIT_LEADING = '>'
    bar._Bar__CHAR_UNIT_FULL = '='
    bar._Bar__CHAR_UNIT_HALF = '-'

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10)

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10, -1)

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10, 100.1)

    assert '[          ]' == getattr(bar, '_Bar__bar')(12, 0)
    assert '[          ]' == getattr(bar, '_Bar__bar')(12, 9)
    assert '[>         ]' == getattr(bar, '_Bar__bar')(12, 10)
    assert '[>         ]' == getattr(bar, '_Bar__bar')(12, 15)
    assert '[=>        ]' == getattr(bar, '_Bar__bar')(12, 20)
    assert '[====>     ]' == getattr(bar, '_Bar__bar')(12, 50)
    assert '[========> ]' == getattr(bar, '_Bar__bar')(12, 99)
    assert '[=========>]' == getattr(bar, '_Bar__bar')(12, 100)


def test_defined_half_and_full():
    bar = Bar()
    bar._Bar__CHAR_UNIT_FULL = '='
    bar._Bar__CHAR_UNIT_HALF = '-'

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10)

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10, -1)

    with pytest.raises(ValueError):
        getattr(bar, '_Bar__bar')(10, 100.1)

    assert '[          ]' == getattr(bar, '_Bar__bar')(12, 0)
    assert '[-         ]' == getattr(bar, '_Bar__bar')(12, 9)
    assert '[=         ]' == getattr(bar, '_Bar__bar')(12, 10)
    assert '[=-        ]' == getattr(bar, '_Bar__bar')(12, 15)
    assert '[==        ]' == getattr(bar, '_Bar__bar')(12, 20)
    assert '[=====     ]' == getattr(bar, '_Bar__bar')(12, 50)
    assert '[=========-]' == getattr(bar, '_Bar__bar')(12, 99)
    assert '[==========]' == getattr(bar, '_Bar__bar')(12, 100)


def test_defined_full_only():
    bar = Bar()

    assert '[          ]' == getattr(bar, '_Bar__bar')(12, 0)
    assert '[          ]' == getattr(bar, '_Bar__bar')(12, 9)
    assert '[#         ]' == getattr(bar, '_Bar__bar')(12, 10)
    assert '[#         ]' == getattr(bar, '_Bar__bar')(12, 15)
    assert '[##        ]' == getattr(bar, '_Bar__bar')(12, 20)
    assert '[#####     ]' == getattr(bar, '_Bar__bar')(12, 50)
    assert '[######### ]' == getattr(bar, '_Bar__bar')(12, 99)
    assert '[##########]' == getattr(bar, '_Bar__bar')(12, 100)


def test_empty_char():
    bar = Bar()
    bar._Bar__CHAR_UNIT_HALF = '.'
    bar._Bar__CHAR_UNIT_EMPTY = '.'

    assert '[..........]' == getattr(bar, '_Bar__bar')(12, 0)
    assert '[..........]' == getattr(bar, '_Bar__bar')(12, 9)
    assert '[#.........]' == getattr(bar, '_Bar__bar')(12, 10)
    assert '[#.........]' == getattr(bar, '_Bar__bar')(12, 15)
    assert '[##........]' == getattr(bar, '_Bar__bar')(12, 20)
    assert '[#####.....]' == getattr(bar, '_Bar__bar')(12, 50)
    assert '[#########.]' == getattr(bar, '_Bar__bar')(12, 99)
    assert '[##########]' == getattr(bar, '_Bar__bar')(12, 100)
