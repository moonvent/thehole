import pygame
from pygame.event import EventType
import pygame.locals as pg_consts

from logic.game_objects.character._character import _Character
from logic.game_objects.character._map_position import Position


class Player(_Character):
    def __init__(self):
        super().__init__()
        self.spawn_point = Position(0, 0)

    def moving(self):
        keys = pygame.key.get_pressed()
        if keys[pg_consts.K_UP]:
            self.move_up()
        if keys[pg_consts.K_DOWN]:
            self.move_down()
        if keys[pg_consts.K_LEFT]:
            self.move_left()
        if keys[pg_consts.K_RIGHT]:
            self.move_right()
        self.update()
        self.stop()

