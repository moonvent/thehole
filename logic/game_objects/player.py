import pygame
from pygame.event import EventType
import pygame.locals as pg_consts

from logic.game_objects.character._character import _Character
from logic.game_objects.character._map_position import Position
from logic.game_objects.character._moving import _PlayerMovingMixin


class Player(_Character, _PlayerMovingMixin):
    def __init__(self):
        super().__init__()
        _PlayerMovingMixin.__init__(self)
        self.spawn_point = Position(0, 0)

    def moving(self):
        super(Player, self).moving()
        self.update()
        self.stop(swap_sprite=False)

