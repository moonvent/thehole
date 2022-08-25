import pygame

from logic.game_objects.map.map import Map
from logic.game_objects.player import Player
from services.load_resources import load_image


class World:
    """
        Общий класс для всего мира
    """
    level: Map = None
    player: Player = None

    def __init__(self, screen: pygame.Surface):
        self.player = Player()
        self.level = Map(surface=screen)

