import pygame

from logic.game_objects.player import Player
from services.load_resources import load_image


class World:
    """
        Общий класс для всего мира
    """
    background: pygame.Surface = None

    def __init__(self, screen: pygame.Surface):
        # self.background = pygame.Surface(screen.get_size())
        self.background, _ = load_image('1.jpg')
        self.background = self.background.convert()
        # self.background.fill((255, 255, 255))

        self.player = Player()

