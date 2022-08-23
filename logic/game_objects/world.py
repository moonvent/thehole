import pygame

from logic.game_objects.player import Player


class World:
    """
        Общий класс для всего мира
    """
    background: pygame.Surface = None

    def __init__(self, screen):
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.player = Player()

