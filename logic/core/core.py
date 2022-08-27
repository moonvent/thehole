import pygame
import pygame as pg
from pygame.event import EventType
from pygame.surface import Surface

from logic.game_objects.world import World
from services.constants import GameConstants

import pygame.locals as pg_consts


class Core:
    def __init__(self):
        pg.init()

        pg.display.set_caption(GameConstants.Title)
        # self.screen: Surface = pg.display.set_mode((0, 0),
        #                                            pygame.FULLSCREEN)
        self.screen: Surface = pg.display.set_mode((1920, 1080))
        self.world = World(screen=self.screen)
        self.player = self.world.player
        self.level = self.world.level

    def start(self):
        clock = pygame.time.Clock()
        self.level.draw()
        # self.refresh_screen()
        pg.display.flip()

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
        self.player.moving(surface=self.level.get_current_surface(self.player))

    def refresh_screen(self):
        from_point, to_point = self.level.repaint(player=self.world.player)
        self.screen.blit(self.world.player.image,
                         self.world.player.rect,)
        self.level.update_after_player()

        pg.display.update(pygame.Rect(*from_point, *to_point))
