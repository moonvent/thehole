from enum import IntEnum
from typing import NamedTuple

from pygame import Rect

from src.logic.game_objects.character.mechanics.action import ActionType
from pygame.sprite import Sprite
from pygame.surface import Surface

from src.logic.game_objects.map.level import MapLevel
from src.logic.game_objects.character.mechanics.directions import MoveDirection, DirectionsConsts
from src.logic.game_objects.map.location_patterns import Literals
from src.services.constants import GameConstants


class MapElementLoadType(NamedTuple):
    path: str | tuple[str, ...]
    directions: tuple[MoveDirection]
    available_walk_side: tuple[Rect, ...]

    action_type: ActionType = ActionType.usual
    map_level: MapLevel = MapLevel.Usual


class RectTypes:
    AllRect = (Rect(0, 0, GameConstants.WidthMapElement, GameConstants.HeightMapElement),)
    NoRect = ()

    HalfHighGround = (Rect(0, 55, GameConstants.WidthMapElement, GameConstants.HeightMapElement - 65 - 52),)

    LeftToRightUp = (Rect(0, 100, GameConstants.WidthMapElement, GameConstants.HeightMapElement),
                     Rect(50, 60, GameConstants.WidthMapElement, GameConstants.HeightMapElement),)
    RightToLeftUp = (Rect(50, 110, GameConstants.WidthMapElement, GameConstants.HeightMapElement),
                     Rect(0, 50, 100, GameConstants.HeightMapElement))

    TopHighGround = (Rect(0, 0, GameConstants.WidthMapElement, GameConstants.HeightMapElement),)
    BotHighGround = (Rect(0, 0, GameConstants.WidthMapElement, GameConstants.HeightMapElement - 65),)


class ElementAvailability(IntEnum):
    """
        Действия при переходе на следующий элемент;

    """
    NoStep = 0
    Step = 1
    MapBorder = 2
    Home = 3



MapElements = {
               # 'a': MapElementLoadType('tileGrass_slope_half.png', DirectionsConsts.AllDirections),
               Literals.b: MapElementLoadType('tileGrass_slopeLeft_grass.png',
                                              DirectionsConsts.XMoving,
                                              RectTypes.LeftToRightUp,
                                              action_type=ActionType.lifting_up),
               Literals.c: MapElementLoadType('tileGrass_slopeRight_grass.png', DirectionsConsts.XMoving, RectTypes.RightToLeftUp, action_type=ActionType.lifting_down),
               Literals.d: MapElementLoadType('tileGrass_grass.png', DirectionsConsts.AllDirections, RectTypes.HalfHighGround, map_level=MapLevel.ElevationUp),
               Literals.e: MapElementLoadType(('grass.png',
                                               'foliageFewTree_green.png'), DirectionsConsts.AllDirections, RectTypes.AllRect),
               Literals.f: MapElementLoadType(('grass.png',
                                              'few_trees_2.png'), DirectionsConsts.AllDirections, RectTypes.AllRect),
               Literals.g: MapElementLoadType('grass.png', DirectionsConsts.AllDirections, RectTypes.AllRect, ),
               Literals.h: MapElementLoadType('high_ground_green.png', DirectionsConsts.AllDirections, RectTypes.NoRect, map_level=MapLevel.ElevationUp),
               Literals.i: MapElementLoadType('bot_high_ground_green.png', DirectionsConsts.AllDirections, RectTypes.BotHighGround, map_level=MapLevel.ElevationUp),
               Literals.j: MapElementLoadType('top_high_ground_green.png', DirectionsConsts.AllDirections, RectTypes.TopHighGround, map_level=MapLevel.ElevationUp),
               Literals.k: MapElementLoadType('center_high_ground_green.png', DirectionsConsts.AllDirections, RectTypes.AllRect, map_level=MapLevel.ElevationUp),
               Literals.l: MapElementLoadType('big_tileGrass_slopeRight_grass.png', DirectionsConsts.AllDirections, RectTypes.AllRect, action_type=ActionType.lifting_down),
               Literals.m: MapElementLoadType('big_tileGrass_slopeLeft_grass.png', DirectionsConsts.AllDirections, RectTypes.AllRect, action_type=ActionType.lifting_up),
               Literals.n: MapElementLoadType('hg_top_bot.png', DirectionsConsts.AllDirections, RectTypes.BotHighGround, map_level=MapLevel.ElevationUp),
               Literals.o: MapElementLoadType('tileWater_with_grass_1.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationDown),
               Literals.p: MapElementLoadType('tileWater_with_grass_2.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationDown),
               Literals.q: MapElementLoadType('tileWater_with_grass_3.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationDown),
               Literals.r: MapElementLoadType('tileWater_with_water_4.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationDown),
               Literals.s: MapElementLoadType(('grass.png',
                                               'few_trees_4.png'), DirectionsConsts.AllDirections, RectTypes.AllRect),
               Literals.t: MapElementLoadType('roof_with_grass.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationUp),
               Literals.u: MapElementLoadType('castle_center_wall.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationUp),
               Literals.v: MapElementLoadType('wall.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationUp),
               Literals.w: MapElementLoadType('roof.png', DirectionsConsts.NoWay, RectTypes.NoRect, map_level=MapLevel.ElevationUp),
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
    _code: str = None
    _directions: tuple[MoveDirection, ...] = None
    _available_walk_side: tuple[Rect, ...] = None

    def __init__(self,
                 sprite: Sprite,
                 action_type: ActionType,
                 additional_sprites: Sprite | tuple[Sprite],
                 map_level,
                 code: str,
                 directions: tuple[MoveDirection, ...],
                 available_walk_side: tuple[Rect, ...]):
        self._sprite = sprite
        self._action_type = action_type
        self._map_level = map_level
        self._code = code
        self._directions = directions
        self._available_walk_side = available_walk_side

        self.additional_sprites = additional_sprites if isinstance(additional_sprites, tuple) else (additional_sprites,)
        if len(self.additional_sprites) > 1:
            self.above_player = True

    @property
    def available_walk_side(self):
        return self._available_walk_side

    @property
    def code(self):
        """
            Получаем код элемента
        """
        return self._code

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
