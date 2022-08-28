import pytest
from pygame import Surface, display as pg_display


@pytest.fixture
def pygame_init():
    pg_display.init()
    pg_display.set_mode((100, 100))
