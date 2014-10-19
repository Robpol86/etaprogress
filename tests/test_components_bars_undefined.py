from etaprogress.components.bars import BarUndefinedAnimated, BarUndefinedEmpty


def test_empty(request):
    def fin():
        BarUndefinedEmpty.CHAR_LEFT_BORDER = '['
        BarUndefinedEmpty.CHAR_RIGHT_BORDER = ']'
    request.addfinalizer(fin)

    bar = BarUndefinedEmpty()
    assert '[        ]' == bar.bar(10)
    assert '[             ]' == bar.bar(15)

    BarUndefinedEmpty.CHAR_LEFT_BORDER = '[['
    BarUndefinedEmpty.CHAR_RIGHT_BORDER = ']]'
    bar = BarUndefinedEmpty()
    assert '[[      ]]' == bar.bar(10)
    assert '[[           ]]' == bar.bar(15)


def test_animated():
    bar = BarUndefinedAnimated()

    assert '[?       ]' == bar.bar(10)
    assert '[ ?      ]' == bar.bar(10)
    assert '[  ?     ]' == bar.bar(10)
    assert '[   ?    ]' == bar.bar(10)
    assert '[    ?   ]' == bar.bar(10)
    assert '[     ?  ]' == bar.bar(10)
    assert '[      ? ]' == bar.bar(10)
    assert '[       ?]' == bar.bar(10)
    assert '[      ? ]' == bar.bar(10)
    assert '[     ?  ]' == bar.bar(10)
    assert '[    ?   ]' == bar.bar(10)
    assert '[   ?    ]' == bar.bar(10)
    assert '[  ?     ]' == bar.bar(10)
    assert '[ ?      ]' == bar.bar(10)
    assert '[?       ]' == bar.bar(10)
    assert '[ ?      ]' == bar.bar(10)
    assert '[  ?     ]' == bar.bar(10)


def test_undefined_animated_resize():
    bar = BarUndefinedAnimated()

    assert '[?       ]' == bar.bar(10)
    assert '[ ?      ]' == bar.bar(10)
    assert '[  ?     ]' == bar.bar(10)
    assert '[   ?    ]' == bar.bar(10)
    assert '[    ?   ]' == bar.bar(10)
    assert '[     ?  ]' == bar.bar(10)
    assert '[ ? ]' == bar.bar(5)
    assert '[?       ]' == bar.bar(10)
    assert '[ ?      ]' == bar.bar(10)


def test_undefined_animated_large(request):
    def fin():
        BarUndefinedAnimated.CHAR_LEFT_BORDER = '['
        BarUndefinedAnimated.CHAR_RIGHT_BORDER = ']'
        BarUndefinedAnimated.CHAR_ANIMATED = '?'
    request.addfinalizer(fin)

    BarUndefinedAnimated.CHAR_LEFT_BORDER = '<['
    BarUndefinedAnimated.CHAR_RIGHT_BORDER = ']>'
    BarUndefinedAnimated.CHAR_ANIMATED = '<?>'
    bar = BarUndefinedAnimated()

    assert '<[<?>   ]>' == bar.bar(10)
    assert '<[ <?>  ]>' == bar.bar(10)
    assert '<[  <?> ]>' == bar.bar(10)
    assert '<[   <?>]>' == bar.bar(10)
    assert '<[  <?> ]>' == bar.bar(10)
    assert '<[ <?>  ]>' == bar.bar(10)
    assert '<[<?>   ]>' == bar.bar(10)
    assert '<[ <?>  ]>' == bar.bar(10)
    assert '<[  <?> ]>' == bar.bar(10)
