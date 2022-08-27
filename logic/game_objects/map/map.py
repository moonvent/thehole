import os

from pygame import Surface
from pygame.sprite import Sprite, Group

from logic.game_objects.character.player import Player

from logic.game_objects.map.element import MapElement, MapElementInGame, MapElements
from logic.game_objects.map.pattern import pattern
from services.constants import Folders, GameConstants
from services.load_resources import load_image


class Map:
    _elements_group: Group = None
    _display_surface: Surface = None
    _elements: dict[tuple[int, int], MapElementInGame] = None
    _update_after_player: list[Sprite] = None

    def __init__(self, surface: Surface):
        self._elements = {}
        self._display_surface = surface
        self._elements_group = Group()
        self._create_map()

    @property
    def map_surface(self):
        return self._display_surface

    @property
    def map_elements(self):
        return self._elements

    def get_element_by_coords(self, x: int, y: int) -> MapElementInGame:
        x = x // GameConstants.WidthMapElement * GameConstants.WidthMapElement
        y = y // GameConstants.HeightMapElement * GameConstants.HeightMapElement
        return self.map_elements[(x, y)]

    def _create_map(self):
        # self._display_surface.fill()
        for row_number, row in enumerate(pattern):
            for column_number, element in enumerate(row):

                if map_element_const := MapElements.get(element):

                    sprites_path, sprites = [], []
                    if isinstance(map_element_const.path, str):
                        sprites_path.append(map_element_const.path)
                    else:
                        sprites_path = map_element_const.path

                    for path_to_sprite in sprites_path:
                        path_to_image = os.path.join(Folders.Map.value, path_to_sprite)
                        element_preset, _ = load_image(path_to_image)
                        sprites.append(element_preset)

                    x, y = column_number * GameConstants.WidthMapElement, row_number * GameConstants.HeightMapElement

                    map_element = MapElement(x, y, sprites[0])

                    additional_sprites = tuple(MapElement(x, y, surface, constant=True) for surface in sprites[1:])

                    self._elements[(x, y)] = MapElementInGame(sprite=map_element,
                                                              action_type=map_element_const.action_type,
                                                              additional_sprites=additional_sprites,
                                                              map_level=map_element_const.map_level)

                    for map_elem in (map_element, *additional_sprites):
                        self._elements_group.add(map_elem)

    def draw(self):
        self._elements_group.draw(self._display_surface)

    def get_current_surface(self,
                            player: Player) -> MapElementInGame:
        """
            Возвращаем текущую текстуру на которой стоит игрок,
            нужно для взаимодействия игрок -> карта и карта -> игрок
        :param player:
        :return: возвращаем тип текстуры, на которой находится игрок
        """
        actual_coords = player.coords
        current_map_element_player_position = (actual_coords.x //
                                               GameConstants.WidthMapElement *
                                               GameConstants.WidthMapElement,
                                               actual_coords.y //
                                               GameConstants.HeightMapElement *
                                               GameConstants.HeightMapElement)
        return self._elements[current_map_element_player_position]

    def repaint(self,
                player: Player) -> tuple:
        actual_coords = player.coords
        nearby_rects = (-1, 0, 1)
        last_element = from_point = to_point = None

        self._update_after_player = []

        for row_element in nearby_rects:
            for column_element in nearby_rects:

                elements_coords = ((actual_coords.x // GameConstants.WidthMapElement + row_element) * GameConstants.WidthMapElement,
                                   (actual_coords.y // GameConstants.HeightMapElement + column_element) * GameConstants.HeightMapElement)

                if element := self._elements.get(elements_coords):
                    element: MapElementInGame = element

                    self._update_after_player += list(element.additional_sprites)
                    self.map_surface.blit(element.sprite.image,
                                          element.sprite.rect)

                    # для обновления определенной области
                    last_element = element
                    if not from_point:
                        from_point = elements_coords
        else:
            to_point = (last_element.sprite.rect.x + last_element.sprite.rect.width,
                        last_element.sprite.rect.y + last_element.sprite.rect.height,)

        return from_point, to_point

    def update_after_player(self):
        for sprite in self._update_after_player:
            self.map_surface.blit(sprite.image,
                                  sprite.rect)


map_object = Map
