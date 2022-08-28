import pytest

import pygame.locals as pg_const

from src.logic.game_objects.world import World
from tests.logic.game_objects.map.patterns import MovingPatterns


@pytest.fixture
def moving_fixture(pygame_init) -> World:
    return World(screen=pygame_init,
                 map_pattern=MovingPatterns.pattern_1.value)


class TestMoving:

    def test_move_to_elevation_up(self,
                                  moving_fixture):
        player, map = moving_fixture.player, moving_fixture.map
        for i in range(40):
            player.moving(pressed_button=pg_const.K_RIGHT)

        print(player.player_level, player.rect)
        assert map.get_element_by_coords(player.coords.x, player.coords.y).map_level == player.player_level

