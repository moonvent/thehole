import sys

import pygame
import pygame as pg
from pygame.event import EventType
from pygame.surface import Surface

from logic.game_objects.player import Player
from logic.game_objects.world import World
from services.constants import GameConstants

import pygame.locals as pg_consts


class Core:
    def __init__(self):
        pg.init()

        pg.display.set_caption(GameConstants.Title)
        self.screen: Surface = pg.display.set_mode(GameConstants.Size)
        self.world = World(screen=self.screen)
        self.player = self.world.player
        self.level = self.world.level

    def start(self):
        clock = pygame.time.Clock()
        # self.level.draw()

        while True:
            clock.tick(GameConstants.AmountFps)

            self.handle_events()
            self.refresh_screen()

            # if a % 60 == 0:
            #     a = 0
            #     pg.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            event: EventType = event

            if event.type == pg_consts.QUIT:
                return

            if event.type == pg_consts.KEYDOWN:
                ...

            if event.type == pg_consts.KEYUP:
                ...

        self.player_events()

    def player_events(self):
        self.player.moving(action_type=self.level.get_current_surface(self.player.rect))

    def refresh_screen(self):
        self.level.draw()
        self.screen.blit(self.world.player.image,
                         self.world.player.rect,)
        pg.display.flip()
