from typing import Callable

import pygame

from src.logic.game_objects.map.map import Map, map_object
from src.logic.game_objects.character.player import Player
from src.logic.game_objects.map.location_patterns import Locations, locations
from tests.logic.game_objects.map.patterns import MovingPatterns


class World:
    """
        Общий класс для всего мира
    """
    map: Map = None
    player: Player = None

    def __init__(self,
                 screen: pygame.Surface,
                 location: Locations = locations[0],
                 # map_pattern: tuple[str, ...] = MovingPatterns.pattern_1.value
                 ):
        self.player = Player()
        global map_object
        if isinstance(map_object, Callable):
            map_object = map_object(surface=screen,
                                    location=location,
                                    player=self.player)
        self.map = map_object

