from enum import IntEnum
from typing import Callable

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from logic.game_objects.character.action import ActionType
from logic.game_objects.map.element import MapElementInGame, MapElement
from logic.game_objects.map.level import MapLevel
from logic.game_objects.position import _MapPosition, Position, MoveDirection
import pygame.locals as pg_consts

from services.constants import GameConstants


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
                              surface_lift: MapLevel,
                              player_lift: MapLevel,
                              action: ActionType):

        # print(62, surface_lift, player_lift, action)
        match surface_lift:

            case MapLevel.Usual if player_lift == MapLevel.Usual and action == ActionType.lifting_up:
                self.player_level = MapLevel.ElevationUp

            case MapLevel.Usual if player_lift == MapLevel.ElevationDown and action == ActionType.lifting_up:
                self.player_level = MapLevel.Usual

            case MapLevel.Usual if player_lift == MapLevel.ElevationUp and action == action.lifting_up:
                pass

            case MapLevel.Usual if player_lift == MapLevel.Usual and action == ActionType.lifting_down:
                self.player_level = MapLevel.ElevationDown

            case MapLevel.Usual if player_lift == MapLevel.ElevationUp and action == action.lifting_down:
                self.player_level = MapLevel.Usual

            case MapLevel.Usual if player_lift == MapLevel.ElevationDown and action == action.lifting_down:
                pass

            case MapLevel.Usual if player_lift == MapLevel.Usual:
                pass

            case _:
                raise Exception('Необработанная ситуация')


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
                            direction: MoveDirection,
                            current_position: Position) -> bool:
        """
            Проверяем следующую позицию на возможность зайти на неё
        :param current_surface: текущая клетка на которой стоим
        :param direction: в какую сторону идем
        :param current_position: текущее расположение персонажа
        :return: истина или ложь, можно идти или нет
        """

        next_position = self.get_next_character_position(direction=direction,
                                                         current_position=current_position)
        return self.get_next_surface(direction=direction,
                                     next_position=next_position,
                                     current_surface=current_surface)

    def get_next_character_position(self,
                                    direction: MoveDirection,
                                    current_position: Position) -> Position:
        """
            Просчитывание следующей позиции персонажа, после нажатия на кнопку
        :param direction: направление
        :param current_position: текущая позиция
        :return:
        """
        match direction:

            case MoveDirection.Up:
                current_position.y -= self.one_step

            case MoveDirection.Down:
                current_position.y += self.one_step

            case MoveDirection.Left:
                current_position.x -= self.one_step

            case MoveDirection.Right:
                current_position.x += self.one_step

        return current_position

    def get_next_surface(self,
                         direction: MoveDirection,
                         next_position: Position,
                         current_surface: MapElementInGame):
        """
            Получение следующего блока, и проверка его на возможность зайти на него
        :param direction: направления куда двигается персонаж
        :param next_position: следующая позиция куда персонаж хочет пойти
        :param current_surface: текущее место где стоит персонаж
        :return: можно или нет идти на следующий блок
        """
        from logic.game_objects.world import map_object
        current_surace_rect = current_surface.sprite.rect

        need_calculate = False

        match direction:
            case MoveDirection.Up if next_position.y < current_surace_rect.y:
                need_calculate = True
            case MoveDirection.Down if next_position.y > current_surace_rect.y:
                need_calculate = True
            case MoveDirection.Left if next_position.x < current_surace_rect.x:
                need_calculate = True
            case MoveDirection.Right if next_position.x > current_surace_rect.x:
                need_calculate = True

        if need_calculate:
            next_element = map_object.get_element_by_coords(x=next_position.x,
                                                            y=next_position.y)
            if self._last_action == ActionType.usual and next_element.map_level != self.player_level:
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
                                    direction=MoveDirection.Up,
                                    current_position=self.coords):
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
                                    direction=MoveDirection.Down,
                                    current_position=self.coords):
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

        if self.check_next_position(current_surface=surface,
                                    direction=MoveDirection.Left,
                                    current_position=self.coords):
            self.position_left()
            self.move_image(direction=MoveDirection.Left)

            if surface.action_type != ActionType.usual:
                # из-за того что слева направо - главное направление - инвертируем стороны
                self.last_action = ActionType.lifting_up if self._last_action == ActionType.lifting_down else ActionType.lifting_down

            self.position_lifting(direction=MoveDirection.Left,
                                  action_type=surface.action_type)

    def move_right(self, surface: MapElementInGame):

        if self.check_next_position(current_surface=surface,
                                    direction=MoveDirection.Right,
                                    current_position=self.coords):
            self.position_right()
            self.move_image(direction=MoveDirection.Right)

            if surface.action_type != ActionType.usual:
                self.last_action = surface.action_type

            self.position_lifting(direction=MoveDirection.Right,
                                  action_type=surface.action_type)

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

    def moving(self, surface: MapElementInGame):
        keys = pygame.key.get_pressed()

        if pressed_buttons := tuple(move_method
                                    for move_method, button_id in self._directions.items()
                                    if keys[button_id]):
            pressed_buttons[0](surface=surface)

        else:
            self.stop(swap_sprite=True,
                      surface=surface)
