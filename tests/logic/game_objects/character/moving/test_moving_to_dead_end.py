from src.logic.game_objects.map.level import MapLevel
from src.services.constants import GameConstants
import pytest
import pygame.locals as pg_const
from src.logic.game_objects.world import World



CoordsToDeadEndFromTop = ((150, 270),
                          (150, 300),
                          )

CoordsToDeadEndFromLeft = ((40, 440),
                           (100, 440),)

CoordsToDeadEndFromRight = ((290, 440, 20),
                            (290, 440, 200),
                            (290, 440, 100),
                            )

CoordsToDeadEndFromBottom = ((0, 500, 160, 0),
                             (0, 500, 160, 10),
                             (0, 500, 160, 150),
                             )


class TestMovingToDeadEnd:
    # @pytest.mark.skip(reason="Status: Write new test")
    @pytest.mark.parametrize('row_pixels,column_pixels', CoordsToDeadEndFromTop)
    def test_move_to_dead_end_from_top(self,
                                       moving_fixture: World,
                                       row_pixels: int,
                                       column_pixels: int):
        player, map = moving_fixture.player, moving_fixture.map

        for i in range(int(row_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_RIGHT)

        for i in range(int(column_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_DOWN)

        assert (map.get_element_by_coords(player.coords.x, player.coords.y).map_level ==
                player.player_level ==
                MapLevel.Usual)

    # @pytest.mark.skip(reason="Status: Write new test")
    @pytest.mark.parametrize('row_pixels,column_pixels', CoordsToDeadEndFromLeft)
    def test_move_to_dead_end_from_left(self,
                                        moving_fixture: World,
                                        row_pixels: int,
                                        column_pixels: int):
        player, map = moving_fixture.player, moving_fixture.map

        for i in range(int(column_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_DOWN)

        for i in range(int(row_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_RIGHT)

        assert (map.get_element_by_coords(player.coords.x, player.coords.y).map_level ==
                player.player_level ==
                MapLevel.Usual)

    @pytest.mark.parametrize('row_pixels,column_pixels,row_pixels_back', CoordsToDeadEndFromRight)
    def test_move_to_dead_end_from_right(self,
                                         moving_fixture: World,
                                         row_pixels: int,
                                         column_pixels: int,
                                         row_pixels_back: int):
        player, map = moving_fixture.player, moving_fixture.map

        for i in range(int(row_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_LEFT)

        for i in range(int(column_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_DOWN)

        for i in range(int(row_pixels_back / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_LEFT)

        assert (map.get_element_by_coords(player.coords.x, player.coords.y).map_level ==
                player.player_level ==
                MapLevel.Usual)

    @pytest.mark.parametrize('row_pixels,column_pixels,row_pixels_back,column_pixels_back', CoordsToDeadEndFromBottom)
    def test_move_to_dead_end_from_bottom(self,
                                          moving_fixture: World,
                                          row_pixels: int,
                                          column_pixels: int,
                                          row_pixels_back: int,
                                          column_pixels_back: int):
        player, map = moving_fixture.player, moving_fixture.map

        for i in range(int(row_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_UP)

        for i in range(int(column_pixels / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_DOWN)

        for i in range(int(row_pixels_back / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_RIGHT)

        for i in range(int(column_pixels_back / GameConstants.DefaultStepPixels)):
            player.moving(pressed_button=pg_const.K_UP)

        assert (map.get_element_by_coords(player.coords.x, player.coords.y).map_level ==
                player.player_level ==
                MapLevel.Usual)
