from enum import Enum
import os
import pygame

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


class _Character(pygame.sprite.Sprite):
    """
        Character interface
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._load_character()

    def _load_character(self, folder_name: str = GameConstants.DefaulSkinFolder):
        """
            Load all char poses
        :param folder_name: char name from statics/characters
        :return:
        """
        for enum_elem in _CharacterActions:
            setattr(self, f'action_{enum_elem.name}', load_image(path_join(folder_name, enum_elem.value))[0])

        self._default_player_state = self.action_think
        self.image, self.rect = self._default_player_state, self._default_player_state.get_rect()

        self.sprite = pygame.sprite.RenderPlain((self,))
