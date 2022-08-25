import os

from pygame import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite, Group

from logic.game_objects.action import ActionType
from logic.game_objects.player import Player
from logic.game_objects.position import Position

from logic.game_objects.map.map_element import MapElement, MapElementInGame
from logic.game_objects.map.pattern import pattern, MapElementsConsts
from services.constants import Folders, GameConstants
from services.load_resources import load_image


class Map:
    _elements_group: Group = None
    _display_surface: Surface = None
    _elements: dict[tuple[int, int], MapElementInGame] = None

    def __init__(self, surface: Surface):
        self._elements = {}
        self._display_surface = surface
        self._elements_group = Group()
        self._create_map()

    def _create_map(self):

        for row_number, row in enumerate(pattern):
            for column_number, element in enumerate(row):

                if map_element_const := MapElementsConsts.get(element):

                    path_to_image = os.path.join(Folders.Map.value, map_element_const.path)
                    element_preset, _ = load_image(path_to_image)

                    x, y = column_number * GameConstants.WidthMapElement, row_number * GameConstants.HeightMapElement

                    map_element = MapElement(x, y, element_preset)

                    self._elements[(x, y)] = MapElementInGame(sprite=map_element,
                                                              action_type=map_element_const.action_type)

                    self._elements_group.add(map_element)

    def draw(self):
        self._elements_group.draw(self._display_surface)

    def get_current_surface(self,
                            player: Player) -> ActionType:
        """
            Возвращаем текущую текстуру на которой стоит игрок,
            нужно для взаимодействия игрок -> карта и карта -> игрок
        :param player:
        :return: возвращаем тип текстуры, на которой находится игрок
        """
        actual_coords = Position(x=player.x + GameConstants.PlayerWidth / 2,
                                 y=player.y + GameConstants.PlayerHeight / 2)
        current_map_element_player_position = (actual_coords.x //
                                               GameConstants.WidthMapElement *
                                               GameConstants.WidthMapElement,
                                               actual_coords.y //
                                               GameConstants.HeightMapElement *
                                               GameConstants.HeightMapElement)
        return self._elements[current_map_element_player_position].ActionType




