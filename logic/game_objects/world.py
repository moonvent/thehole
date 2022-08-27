import pygame

from logic.game_objects.map.map import Map, map_object
from logic.game_objects.character.player import Player


class World:
    """
        Общий класс для всего мира
    """
    level: Map = None
    player: Player = None

    def __init__(self, screen: pygame.Surface):
        self.player = Player()
        global map_object
        map_object = map_object(surface=screen)
        self.level = map_object

