from src.services.constants import GameConstants
from tests.logic.game_objects.map.patterns import MoveLocation
import pygame
import pytest
from src.logic.game_objects.world import World


@pytest.fixture
def moving_fixture(pygame_init) -> World:
    if GameConstants.DefaultStepPixels != 10:
        raise ValueError('Все тесты были произведены на шаг "10"!')
    yield World(screen=pygame_init,
                location=MoveLocation)
    pygame.quit()
