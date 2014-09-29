import pytest

from etaprogress import eta


DATA_SET = [  # (time, numerator, rate, eta_seconds, percent)

]

@pytest.fixture
def setup_global_eta():
    eta_instance = eta.ETA()