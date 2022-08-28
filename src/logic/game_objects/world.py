from typing import Callable

import pygame

from src.logic.game_objects.map.map import Map, map_object
from src.logic.game_objects.character.player import Player
from src.logic.game_objects.map.pattern import pattern
from tests.logic.game_objects.map.patterns import MovingPatterns


class World:
    """
        Общий класс для всего мира
    """
    map: Map = None
    player: Player = None

    def __init__(self,
                 screen: pygame.Surface,
                 # map_pattern: tuple[str, ...] = pattern,
                 map_pattern: tuple[str, ...] = MovingPatterns.pattern_1.value
                 ):
        self.player = Player()
        global map_object
        if isinstance(map_object, Callable):
            map_object = map_object(surface=screen,
                                    map_pattern=map_pattern)
        self.map = map_object

