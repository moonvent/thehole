import os
from enum import Enum
from typing import NamedTuple

import pygame.locals as pg_consts


class Files(Enum):
    ...


class Folders(Enum):
    Static = 'static'
    Characters = 'characters'
    Map = 'map'


class _GameConstant:
    """
        Константы используемые для игры, размеры экрана, сложность, и т.д.
    """

    class _Size(NamedTuple):
        width: int
        height: int

    Size = _Size(800, 600)

    _amount_fps: int = 60

    @property
    def AmountFps(self):
        return self._amount_fps

    _title = 'Adventure'

    @property
    def Title(self):
        return self._title

    _default_skin_folder: str = os.path.join(Folders.Characters.value,
                                             'Male adventurer')

    @property
    def DefaulSkinFolder(self):
        return self._default_skin_folder

    _default_step_pixels: int = 10

    @property
    def DefaultStepPixels(self):
        return self._default_step_pixels

    _player_moving_buttoms = (pg_consts.K_DOWN,
                              pg_consts.K_UP,
                              pg_consts.K_LEFT,
                              pg_consts.K_RIGHT)

    @property
    def PlayerMovingButtoms(self):
        return self._player_moving_buttoms

    _height_map_element: int = 200
    _width_map_element: int = 128

    @property
    def HeightMapElement(self):
        return self._height_map_element

    @property
    def WidthMapElement(self):
        return self._width_map_element

    _player_width: int = 96
    _player_height: int = 128

    @property
    def PlayerWidth(self):
        return self._player_width

    @property
    def PlayerHeight(self):
        return self._player_height


GameConstants = _GameConstant()
