from src.services.constants import GameConstants
from tests.logic.game_objects.map.patterns import MovingPatterns
import pygame
import pytest
from src.logic.game_objects.world import World


@pytest.fixture
def moving_fixture(pygame_init) -> World:
    if GameConstants.DefaultStepPixels != 10:
        raise ValueError('Все тесты были произведены на шаг "10"!')
    yield World(screen=pygame_init,
                map_pattern=MovingPatterns.pattern_1.value)
    pygame.quit()
