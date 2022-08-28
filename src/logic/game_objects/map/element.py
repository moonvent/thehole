from typing import NamedTuple

from src.logic.game_objects.character.mechanics.action import ActionType
from pygame.sprite import Sprite
from pygame.surface import Surface

from src.logic.game_objects.map.level import MapLevel


class MapElementLoadType(NamedTuple):
    path: str | tuple[str, ...]

    action_type: ActionType = ActionType.usual
    map_level: MapLevel = MapLevel.Usual


MapElements = {'a': MapElementLoadType('tileGrass_slope_half.png'),
               'b': MapElementLoadType('tileGrass_slopeLeft_grass.png', ActionType.lifting_up),
               'c': MapElementLoadType('tileGrass_slopeRight_grass.png', ActionType.lifting_down),
               'd': MapElementLoadType('tileGrass_grass.png', map_level=MapLevel.ElevationUp),
               'e': MapElementLoadType(('grass.png',
                                        'foliageFewTree_green.png')),
               'f': MapElementLoadType('tileGrass_slope.png'),
               'g': MapElementLoadType('grass.png'),
               # 'h': MapElementLoadType('', ActionType.usual),
               # 'i': MapElementLoadType('', ActionType.usual),
               # 'j': MapElementLoadType('', ActionType.usual),
               # 'k': MapElementLoadType('', ActionType.usual),
               # 'l': MapElementLoadType('', ActionType.usual),
               # 'm': MapElementLoadType('', ActionType.usual),
               # 'n': MapElementLoadType('', ActionType.usual),
               # 'o': MapElementLoadType('', ActionType.usual),
               # 'p': MapElementLoadType('', ActionType.usual),
               # 'q': MapElementLoadType('', ActionType.usual),
               # 'r': MapElementLoadType('', ActionType.usual),
               # 's': MapElementLoadType('', ActionType.usual),
               # 't': MapElementLoadType('', ActionType.usual),
               # 'u': MapElementLoadType('', ActionType.usual),
               # 'v': MapElementLoadType('', ActionType.usual),
               # 'w': MapElementLoadType('', ActionType.usual),
               # 'x': MapElementLoadType('', ActionType.usual),
               # 'y': MapElementLoadType('', ActionType.usual),
               # 'z': MapElementLoadType('', ActionType.usual),
               # '1': MapElementLoadType('', ActionType.usual),
               # '2': MapElementLoadType('', ActionType.usual),
               # '3': MapElementLoadType('', ActionType.usual),
               # '4': MapElementLoadType('', ActionType.usual),
               # '5': MapElementLoadType('', ActionType.usual),
               # '6': MapElementLoadType('', ActionType.usual),
               # '7': MapElementLoadType('', ActionType.usual),
               # '8': MapElementLoadType('', ActionType.usual),
               # '9': MapElementLoadType('', ActionType.usual),
               # '0': MapElementLoadType('', ActionType.usual),
               # 'A': MapElementLoadType('', ActionType.usual),
               # 'B': MapElementLoadType('', ActionType.usual),
               # 'C': MapElementLoadType('', ActionType.usual),
               # 'D': MapElementLoadType('', ActionType.usual),
               # 'E': MapElementLoadType('', ActionType.usual),
               # 'F': MapElementLoadType('', ActionType.usual),
               # 'G': MapElementLoadType('', ActionType.usual),
               # 'H': MapElementLoadType('', ActionType.usual),
               # 'I': MapElementLoadType('', ActionType.usual),
               # 'J': MapElementLoadType('', ActionType.usual),
               # 'K': MapElementLoadType('', ActionType.usual),
               # 'L': MapElementLoadType('', ActionType.usual),
               # 'M': MapElementLoadType('', ActionType.usual),
               # 'N': MapElementLoadType('', ActionType.usual),
               }


class MapElement(Sprite):
    constant: bool = False  # будет ли накладываться картинка поверх персонажа

    def __init__(self,
                 x: int,
                 y: int,
                 image: Surface,
                 constant: bool = False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.constant = constant


class MapElementInGame:
    _sprite: Sprite = None
    _action_type: ActionType = None
    _above_player: bool = False
    additional_sprites: tuple[Sprite] = None
    _map_level: MapLevel = None

    def __init__(self,
                 sprite: Sprite,
                 action_type: ActionType,
                 additional_sprites: Sprite | tuple[Sprite],
                 map_level):
        self._sprite = sprite
        self._action_type = action_type
        self._map_level = map_level

        self.additional_sprites = additional_sprites if isinstance(additional_sprites, tuple) else (additional_sprites,)
        if len(self.additional_sprites) > 1:
            self.above_player = True

    @property
    def map_level(self):
        return self._map_level

    @property
    def sprite(self):
        return self._sprite

    @property
    def action_type(self):
        return self._action_type

    @property
    def above_player(self):
        return self._above_player

    @above_player.setter
    def above_player(self, value):
        self.above_player = value
