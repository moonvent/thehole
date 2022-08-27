from dataclasses import dataclass, astuple
from enum import Enum
import os

import pygame

from logic.game_objects.position import Position
from services.constants import GameConstants
from services.load_resources import load_image

path_join = os.path.join


class _CharacterActions(Enum):
    walk_0 = 'walk0.png'
    walk_1 = 'walk1.png'
    walk_2 = 'walk2.png'
    walk_3 = 'walk3.png'
    walk_4 = 'walk4.png'
    walk_5 = 'walk5.png'
    walk_6 = 'walk6.png'
    walk_7 = 'walk7.png'

    back = 'back.png'

    climb0 = 'climb0.png'
    climb1 = 'climb1.png'

    drag = 'drag.png'

    duck = 'duck.png'

    interact = 'interact.png'

    talk = 'talk.png'

    think = 'think.png'

    attack_0 = 'attack0.png'
    attack_1 = 'attack1.png'
    attack_2 = 'attack2.png'

    front_walk_0 = 'switch0.png'
    front_walk_1 = 'switch1.png'

    side = 'side.png'


class Character(pygame.sprite.Sprite):
    """
        Character interface
    """
    _handle_point: Position = None

    def __init__(self, spawn_point: Position):
        super().__init__()
        self.spawn_point = spawn_point
        self._load_character_assets()
        self.handle_point = self.rect.midbottom

    def _load_character_assets(self, folder_name: str = GameConstants.DefaulSkinFolder):
        """
            Load all char poses
        :param folder_name: char name from statics/characters
        :return:
        """

        self.one_step = GameConstants.DefaultStepPixels

        for enum_elem in _CharacterActions:
            setattr(self, f'action_{enum_elem.name}', load_image(path_join(folder_name, enum_elem.value))[0])

        # для обычного простоя с левой стороны
        self.action_flip_side = pygame.transform.flip(self.action_side, True, False)

        self._default_player_state = self.action_think
        self.image, self.rect = self._default_player_state, self._default_player_state.get_rect()

        self.sprite = pygame.sprite.RenderPlain((self,))

    def update(self):
        self.rect = self.rect.move(astuple(self.next_position))
        pygame.event.pump()

    @property
    def coords(self) -> Position:
        return Position(self.rect.x + self.handle_point.x,
                        self.rect.y + self.handle_point.y)

    @coords.setter
    def coords(self, value):
        raise NotImplemented

    @property
    def handle_point(self):
        return self._handle_point

    @handle_point.setter
    def handle_point(self,
                     value: tuple[int, int] | Position):
        if not isinstance(value, Position) and \
                not isinstance(value, tuple) or \
                len(value) != 2:
            raise TypeError('"handle_point" должен быть типа "Position" или "tuple" с двумя элементами')

        self._handle_point = value if isinstance(value, Position) else Position(*value)