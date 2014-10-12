import locale

import pytest

from etaprogress import eta, progress_components
from etaprogress.progress import ProgressBarWget


@pytest.fixture(autouse=True, scope='module')
def define_locale():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def test_undefined():
    progress_components.DEFAULT_TERMINAL_WIDTH = 60
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarWget(None, max_width=55)

    assert '    [<=>          ] 0           --.-KiB/s              ' == progress_bar.bar
    assert '    [ <=>         ] 0           --.-KiB/s              ' == progress_bar.bar
    assert '    [  <=>        ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(10)
    assert '    [   <=>       ] 10          --.-KiB/s              ' == progress_bar.bar
    assert '    [    <=>      ] 10          --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(100)
    assert '    [     <=>     ] 100            180B/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(1954727)
    assert '    [      <=>    ] 1,954,727   1.86MiB/s              ' == progress_bar.bar
    assert '    [       <=>   ] 1,954,727   1.86MiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(4217583)
    assert '    [        <=>  ] 4,217,583   2.79MiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(6826725)
    assert '    [         <=> ] 6,826,725   3.41MiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(8659265)
    assert '    [          <=>] 8,659,265   3.60MiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.0
    progress_bar.eta.set_numerator(8659265)
    assert '    [         <=> ] 8,659,265   3.28MiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.5
    progress_bar.eta.set_numerator(21057295)
    assert '    [        <=>  ] 21,057,295  4.85MiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868726.0
    progress_bar.eta.set_numerator(65572196)
    assert '    [       <=>   ] 65,572,196  10.9MiB/s              ' == progress_bar.bar

    progress_bar.done = True
    assert '    [      <=>    ] 65,572,196  13.9MiB/s   in 5s      ' == progress_bar.bar


def test_defined():
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarWget(2000)

    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar
    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar
    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(102)
    assert ' 5% [                  ] 102         --.-KiB/s              ' == progress_bar.bar
    assert ' 5% [                  ] 102         --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(281)
    assert '14% [=>                ] 281            358B/s  eta 5s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(593)
    assert '29% [====>             ] 593            491B/s  eta 3s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(1925)
    assert '96% [================> ] 1,925       1.13KiB/s  eta 1s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(1999)
    assert '99% [================> ] 1,999       1.06KiB/s  eta 1s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(2000)
    assert '100%[=================>] 2,000          666B/s   in 3s      ' == progress_bar.bar


def test_defined_rounded():
    eta._NOW = lambda: 1411868723.5
    progress_bar = ProgressBarWget(1023)

    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(1022)
    assert '99% [================> ] 1,022       --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(1023)
    assert '100%[=================>] 1,023       --.-KiB/s   in 1s      ' == progress_bar.bar


def test_defined_hour():
    progress_bar = ProgressBarWget(2000)

    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert ' 0% [                  ] 1           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(2)
    assert ' 0% [                  ] 2             0.50B/s  eta 1h 6m   ' == progress_bar.bar


def test_defined_weeks():
    progress_bar = ProgressBarWget(2000000000)

    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert ' 0% [                  ] 1           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(2)
    assert ' 0% [                  ] 2             0.50B/s  eta 6613w 5d' == progress_bar.bar


def test_defined_wont_fit():
    progress_bar = ProgressBarWget(2000, max_width=33)
    assert ' 0% [] 0           --.-KiB/s              ' == progress_bar.bar

    progress_bar = ProgressBarWget(2000, max_width=30)
    assert ' 0% [] 0           --.-KiB/s              ' == progress_bar.bar


def test_overflow_eta_caching():
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarWget(500000000000, eta_every=4)
    assert ' 0% [                  ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1000000)
    assert ' 0% [                  ] 1,000,000   --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(3000000)
    assert ' 0% [                  ] 3,000,000   3.81MiB/s  eta 1d 10h  ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(6000000)
    assert ' 0% [                  ] 6,000,000   4.77MiB/s  eta 1d 10h  ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(13000000)
    assert ' 0% [                  ] 13,000,000  7.44MiB/s  eta 1d 10h  ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(93000000)
    assert ' 0% [                  ] 93,000,000  37.0MiB/s  eta 1d 10h  ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(193000000)
    assert ' 0% [                  ] 193,000,000 67.4MiB/s  eta 1h 57m  ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.0
    progress_bar.eta.set_numerator(300000000)
    assert ' 0% [                  ] 300,000,000 92.9MiB/s  eta 1h 57m  ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.5
    progress_bar.eta.set_numerator(700000000)
    assert ' 0% [                  ] 700,000,000  159MiB/s  eta 1h 57m  ' == progress_bar.bar

    eta._NOW = lambda: 1411868726.0
    progress_bar.eta.set_numerator(1400000000)
    assert ' 0% [                ] 1,400,000,000  268MiB/s  eta 1h 57m  ' == progress_bar.bar

    eta._NOW = lambda: 1411868726.5
    progress_bar.eta.set_numerator(2500000000)
    assert ' 0% [                ] 2,500,000,000  424MiB/s  eta 18m 41s ' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(9999999999)
    assert ' 1% [                ] 9,999,999,999 1.11GiB/s  eta 18m 41s ' == progress_bar.bar

    eta._NOW = lambda: 1411868727.5
    progress_bar.eta.set_numerator(10000000000)
    assert ' 2% [               ] 10,000,000,000 1.47GiB/s  eta 18m 41s ' == progress_bar.bar

    eta._NOW = lambda: 1411868728.0
    progress_bar.eta.set_numerator(10000000001)
    assert ' 2% [               ] 10,000,000,001 1.64GiB/s  eta 18m 41s ' == progress_bar.bar

    eta._NOW = lambda: 1411868728.5
    progress_bar.eta.set_numerator(10000000002)
    assert ' 2% [               ] 10,000,000,002 1.70GiB/s  eta 4m 29s  ' == progress_bar.bar

    eta._NOW = lambda: 1411868729.0
    progress_bar.eta.set_numerator(100000000002)
    assert '20% [=>            ] 100,000,000,002 5.89GiB/s  eta 4m 29s  ' == progress_bar.bar

    eta._NOW = lambda: 1411868729.0
    progress_bar.eta.set_numerator(400000000002)
    assert '80% [==========>   ] 400,000,000,002 19.9GiB/s  eta 4m 29s  ' == progress_bar.bar

    eta._NOW = lambda: 1411868729.0
    progress_bar.eta.set_numerator(500000000000)
    assert '100%[=============>] 500,000,000,000 62.1GiB/s   in 8s      ' == progress_bar.bar


def test_defined_long():
    progress_components.DEFAULT_TERMINAL_WIDTH = 45
    eta._NOW = lambda: 1411868721.5
    progress_bar = ProgressBarWget(20)

    assert ' 0% [   ] 0           --.-KiB/s              ' == progress_bar.bar
    assert ' 0% [   ] 0           --.-KiB/s              ' == progress_bar.bar
    assert ' 0% [   ] 0           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.0
    progress_bar.eta.set_numerator(1)
    assert ' 5% [   ] 1           --.-KiB/s              ' == progress_bar.bar
    assert ' 5% [   ] 1           --.-KiB/s              ' == progress_bar.bar

    eta._NOW = lambda: 1411868722.5
    progress_bar.eta.set_numerator(2)
    assert '10% [   ] 2             2.00B/s  eta 9s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.0
    progress_bar.eta.set_numerator(3)
    assert '15% [   ] 3             2.00B/s  eta 9s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868723.5
    progress_bar.eta.set_numerator(4)
    assert '20% [   ] 4             2.00B/s  eta 8s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.0
    progress_bar.eta.set_numerator(5)
    assert '25% [   ] 5             2.00B/s  eta 8s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868724.5
    progress_bar.eta.set_numerator(6)
    assert '30% [   ] 6             2.00B/s  eta 7s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.0
    progress_bar.eta.set_numerator(7)
    assert '35% [>  ] 7             2.00B/s  eta 7s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868725.5
    progress_bar.eta.set_numerator(8)
    assert '40% [>  ] 8             2.00B/s  eta 6s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868726.0
    progress_bar.eta.set_numerator(9)
    assert '45% [>  ] 9             2.00B/s  eta 6s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868726.5
    progress_bar.eta.set_numerator(10)
    assert '50% [>  ] 10            2.00B/s  eta 5s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868727.0
    progress_bar.eta.set_numerator(11)
    assert '55% [>  ] 11            2.00B/s  eta 5s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868727.5
    progress_bar.eta.set_numerator(12)
    assert '60% [>  ] 12            2.00B/s  eta 4s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868728.0
    progress_bar.eta.set_numerator(13)
    assert '65% [>  ] 13            2.00B/s  eta 4s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868728.5
    progress_bar.eta.set_numerator(14)
    assert '70% [=> ] 14            2.00B/s  eta 3s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868729.0
    progress_bar.eta.set_numerator(15)
    assert '75% [=> ] 15            2.00B/s  eta 3s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868729.5
    progress_bar.eta.set_numerator(16)
    assert '80% [=> ] 16            2.00B/s  eta 2s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868730.0
    progress_bar.eta.set_numerator(17)
    assert '85% [=> ] 17            2.00B/s  eta 2s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868730.5
    progress_bar.eta.set_numerator(18)
    assert '90% [=> ] 18            2.00B/s  eta 1s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868731.0
    progress_bar.eta.set_numerator(19)
    assert '95% [=> ] 19            2.00B/s  eta 1s      ' == progress_bar.bar

    eta._NOW = lambda: 1411868731.5
    progress_bar.eta.set_numerator(20)
    assert '100%[==>] 20            2.00B/s   in 10s     ' == progress_bar.bar
