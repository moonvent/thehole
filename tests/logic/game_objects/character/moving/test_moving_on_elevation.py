import pygame.locals as pg_const
from src.logic.game_objects.map.level import MapLevel
from src.logic.game_objects.world import World


class TestMovingElevation:

    # @pytest.mark.skip(reason="Status: Write new test")
    def test_move_to_elevation_up(self,
                                  moving_fixture: World):
        player, map = moving_fixture.player, moving_fixture.map

        for i in range(40):
            # 40 - константа для похода на равнину на карте MovingPatterns.pattern_1.value (* на длину шага)
            player.moving(pressed_button=pg_const.K_RIGHT)

        assert (map.get_element_by_coords(player.coords.x, player.coords.y).map_level ==
                player.player_level ==
                MapLevel.ElevationUp)

