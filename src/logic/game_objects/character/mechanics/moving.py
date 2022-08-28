import random
from typing import Optional

import pygame
from pygame.surface import Surface

from src.logic.game_objects.character.mechanics.action import ActionType
from src.logic.game_objects.map.element import MapElementInGame
from src.logic.game_objects.map.level import MapLevel
from src.logic.game_objects.position import _MapPosition, MoveDirection
import pygame.locals as pg_consts

from src.services.constants import GameConstants


class _Lifting:
    _player_level: MapLevel = MapLevel.Usual

    @property
    def player_level(self):
        return self._player_level

    @player_level.setter
    def player_level(self, lifting_direction: MapLevel):
        if not isinstance(lifting_direction, MapLevel):
            raise ValueError('lifting_direction должно быть "MapLevel" типа')

        self._player_level = lifting_direction

    def change_player_lifting(self,
                              direction: MoveDirection.Left | MoveDirection.Right,
                              surface_level: MapLevel,
                              player_action: ActionType):

        if direction == MoveDirection.Left:
            if player_action == ActionType.lifting_down and surface_level == MapLevel.ElevationUp:
                self.player_level = MapLevel.ElevationUp

            if player_action == ActionType.lifting_up and surface_level == MapLevel.Usual:
                self.player_level = MapLevel.Usual

        else:
            if player_action == ActionType.lifting_down and surface_level == MapLevel.Usual:
                self.player_level = MapLevel.Usual

            if player_action == ActionType.lifting_up and surface_level == MapLevel.ElevationUp:
                self.player_level = MapLevel.ElevationUp


class _ImageMoving:
    _frames_for_walk: list[Surface] = None

    def move_image(self, direction: MoveDirection):

        match direction:

            case MoveDirection.Up:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_back,] * 4 + \
                                           [pygame.transform.flip(self.action_back, True, False),] * 4

                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = MoveDirection.Up

            case MoveDirection.Down:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_front_walk_0,] * 4 + \
                                           [self.action_front_walk_1,] * 4
                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = MoveDirection.Down

            case MoveDirection.Right | MoveDirection.Left:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_walk_0, self.action_walk_1, self.action_walk_2,
                                             self.action_walk_3, self.action_walk_4, self.action_walk_5,
                                             self.action_walk_6, self.action_walk_7,]
                    if direction == MoveDirection.Left:
                        self._frames_for_walk = [pygame.transform.flip(action, True, False) for action in self._frames_for_walk]

                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = direction

            case MoveDirection.Stop:

                if self._last_move_direction != MoveDirection.Up:

                    image = self.action_side
                    if self._last_move_direction == MoveDirection.Left:
                        image = self.action_flip_side

                    self.image = image


class _PreparingToNextStep:
    """
        Класс в котором расписаны методы просчитывания куда пойдет игрок на один блок,
        для того чтоб не заходил на возвышености
    """
    _last_action: ActionType = None

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, value: ActionType):
        if not isinstance(value, ActionType):
            raise TypeError('"_last_action" должен быть типа "ActionType"')
        self._last_action = value

    def check_next_position(self,
                            current_surface: MapElementInGame,
                            direction: MoveDirection) -> bool:
        """
            Получение следующего блока, и проверка его на возможность зайти на него
        :param direction: направления куда двигается персонаж
        :param current_surface: текущее место где стоит персонаж
        :return: можно или нет идти на следующий блок
        """
        from src.logic.game_objects.world import map_object
        current_surace_rect = current_surface.sprite.rect

        x, y = 0, 0

        match direction:
            case MoveDirection.Up if self.rect.top < current_surace_rect.y:
                x, y = self.rect.centerx, self.rect.bottom - GameConstants.DefaultStepPixels
            case MoveDirection.Down if self.rect.bottom > current_surace_rect.y:
                x, y = self.rect.centerx, self.rect.bottom + GameConstants.DefaultStepPixels
            case MoveDirection.Left if self.rect.left < current_surace_rect.x:
                x, y = self.rect.left, self.rect.bottom
            case MoveDirection.Right if self.rect.right > current_surace_rect.x:
                x, y = self.rect.right, self.rect.bottom

        if x and y:
            next_element = map_object.get_element_by_coords(x=x,
                                                            y=y)
            # next_element.sprite.image = Surface((128, 200))
            # next_element.sprite.image.fill((random.randint(1, 255), 0, 0))
            # next_element.sprite.rect = next_element.sprite.image.get_rect()
            # next_element.sprite.rect.x = 128
            # next_element.sprite.rect.y = 400
            # print(next_element.sprite.rect)
            # print(x, y)
            # попробуй collide

            if not next_element:
                return False

            if self.last_action == ActionType.usual and next_element.map_level != self.player_level:
                return False

        return True


class _Moving(_MapPosition,
              _Lifting,
              _ImageMoving,
              _PreparingToNextStep):
    """
        Класс для перемещения персонажа
    """
    _current_direction: MoveDirection = MoveDirection.Right
    _last_move_direction: MoveDirection = None

    @property
    def direction(self):
        return self._current_direction

    @direction.setter
    def direction(self, new_direction: MoveDirection):
        if not isinstance(new_direction, MoveDirection):
            raise ValueError('new_direction is not "MoveDirection" type')
        self._current_direction = new_direction

    def move_up(self, surface: MapElementInGame):

        self.last_action = ActionType.usual

        move = False

        if self.check_next_position(current_surface=surface,
                                    direction=MoveDirection.Up):
            # когда на том же уровне что и карта
            move = True

        elif surface.map_level == MapLevel.ElevationUp and self._last_action == ActionType.lifting_up:
            # когда уже на возвышенности
            if self.coords.y > surface.sprite.rect.y + GameConstants.HeightMapElement - GameConstants.HighGroundTopHeight:
                move = True

        if move:
            self.position_up()
            self.move_image(direction=MoveDirection.Up)

    def move_down(self, surface: MapElementInGame):

        self.last_action = ActionType.usual

        move = False

        if self.check_next_position(current_surface=surface,
                                    direction=MoveDirection.Down):
            # когда на том же уровне что и карта
            move = True

        elif surface.map_level == MapLevel.ElevationUp and self._last_action == ActionType.lifting_up:
            # когда уже на возвышенности
            if self.coords.y < surface.sprite.rect.y + GameConstants.HeightMapElement - GameConstants.HighGroundBottomHeight:
                move = True

        if move:
            self.position_down()
            self.move_image(direction=MoveDirection.Down)

    def move_left(self, surface: MapElementInGame):
        direction = MoveDirection.Left

        if self.check_next_position(current_surface=surface,
                                    direction=direction):
            self.position_left()
            self.move_image(direction=direction)

            if surface.action_type != ActionType.usual:
                # из-за того что слева направо - главное направление - инвертируем стороны
                self.last_action = ActionType.lifting_up if self._last_action == ActionType.lifting_down else ActionType.lifting_down

            self.position_lifting(direction=direction,
                                  action_type=surface.action_type)

            self.change_player_lifting(direction=direction,
                                       surface_level=surface.map_level,
                                       player_action=self.last_action)

    def move_right(self, surface: MapElementInGame):
        direction = MoveDirection.Right

        if self.check_next_position(current_surface=surface,
                                    direction=direction):
            self.position_right()
            self.move_image(direction=direction)

            if surface.action_type != ActionType.usual:
                self.last_action = surface.action_type

            if self.last_action == ActionType.lifting_up and surface.map_level == MapLevel.ElevationUp:
                self.player_level = MapLevel.ElevationUp

            self.position_lifting(direction=direction,
                                  action_type=surface.action_type)

            self.change_player_lifting(direction=direction,
                                       surface_level=surface.map_level,
                                       player_action=self.last_action)


    def stop(self,  surface: MapElementInGame, swap_sprite: bool = True):
        self.position_stop()
        if swap_sprite:
            self.move_image(MoveDirection.Stop)


class PlayerMovingMixin(_Moving):
    """
        Привязка перещмения игрока к перемещению игрока по кнопкам;
    """
    _directions: dict = None

    def __init__(self):
        self._directions = {self.move_up: pg_consts.K_UP,
                            self.move_down: pg_consts.K_DOWN,
                            self.move_left: pg_consts.K_LEFT,
                            self.move_right: pg_consts.K_RIGHT,}

    def moving(self,
               surface: MapElementInGame,
               pressed_button: int | None = None):

        if pressed_button and pressed_button in GameConstants.PlayerMovingButtoms:
            keys = {pressed_button: True}
        else:
            keys = pygame.key.get_pressed()

        if pressed_buttons := tuple(move_method
                                    for move_method, button_id in self._directions.items()
                                    if (isinstance(keys, dict) and keys.get(button_id)) or
                                       (not isinstance(keys, dict) and keys[button_id])):
            pressed_buttons[0](surface=surface)

        else:
            self.stop(swap_sprite=True,
                      surface=surface)
