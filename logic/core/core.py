import sys

import pygame
import pygame as pg
from pygame.event import EventType
from pygame.surface import Surface

from logic.game_objects.player import Player
from logic.game_objects.world import World
from services.constants import GameConstants

from pygame.locals import KEYDOWN as event_keydown


class Core:
    def __init__(self):
        pg.init()

        pg.display.set_caption(GameConstants.Title)
        self.screen: Surface = pg.display.set_mode(GameConstants.Size)
        self.world = World(screen=self.screen)

    def start(self):
        pg.init()

        pg.display.set_caption(GameConstants.Title)
        self.screen = pg.display.set_mode(GameConstants.Size)
        # self.world = World(screen=self.screen)

        clock = pygame.time.Clock()

        while True:
            clock.tick(GameConstants.AmountFps)
            self.handle_events()
            self.refresh_screen()

    def handle_events(self):
        for event in pygame.event.get():
            event: EventType = event

            if event.type == event_keydown:
                print(event.key)

            # if event.type == QUIT:
            #     return

    def refresh_screen(self):
        self.screen.blit(self.world.background,
                         self.world.player.rect,
                         self.world.player.rect)
        self.world.player.sprite.update()
        self.world.player.sprite.draw(self.world.background)
        pg.display.flip()
