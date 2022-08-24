from enum import Enum
from typing import NamedTuple

import pygame
from pygame.surface import Surface

from logic.game_objects.character._map_position import _MapPosition, Position
import pygame.locals as pg_consts


class _MoveDirection(Enum):
    Left = 'left'
    Right = 'right'
    Up = 'up'
    Down = 'down'
    Stop = 'stop'


class _Moving(_MapPosition):
    """
        Класс для перемещения персонажа
    """
    _last_move_direction: _MoveDirection = None
    _frames_for_walk: list[Surface] = None

    def _move(self, direction: _MoveDirection = None):
        match direction:
            case _MoveDirection.Up:
                self.next_position.y = self.next_position.y - self._one_step
            case _MoveDirection.Down:
                self.next_position.y = self.next_position.y + self._one_step
            case _MoveDirection.Left:
                self.next_position.x = self.next_position.x - self._one_step
            case _MoveDirection.Right:
                self.next_position.x = self.next_position.x + self._one_step
            case _MoveDirection.Stop:
                self.next_position = Position(0, 0)

            case _:
                self.next_position = Position(0, 0)
                return

        self.move_image(direction=direction)

    def move_up(self):
        self._move(direction=_MoveDirection.Up)

    def move_down(self):
        self._move(direction=_MoveDirection.Down)

    def move_left(self):
        self._move(direction=_MoveDirection.Left)

    def move_right(self):
        self._move(direction=_MoveDirection.Right)

    def move_image(self, direction: _MoveDirection):

        match direction:

            case _MoveDirection.Up:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_back,] * 4 + \
                                           [pygame.transform.flip(self.action_back, True, False),] * 4

                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = _MoveDirection.Up

            case _MoveDirection.Down:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_front_walk_0,] * 4 + \
                                           [self.action_front_walk_1,] * 4
                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = _MoveDirection.Down

            case _MoveDirection.Right | _MoveDirection.Left:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_walk_0, self.action_walk_1, self.action_walk_2,
                                             self.action_walk_3, self.action_walk_4, self.action_walk_5,
                                             self.action_walk_6, self.action_walk_7,]
                    if direction == _MoveDirection.Left:
                        self._frames_for_walk = [pygame.transform.flip(action, True, False) for action in self._frames_for_walk]

                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = direction

            case _MoveDirection.Stop:

                if self._last_move_direction != _MoveDirection.Up:

                    image = self.action_side
                    if self._last_move_direction == _MoveDirection.Left:
                        image = self.action_flip_side

                    self.image = image

    def stop(self, swap_sprite: bool = True):
        self._move(_MoveDirection.Stop if swap_sprite else None)


class _PlayerMovingMixin(_Moving):

    _directions: dict = None

    def __init__(self):
        self._directions = {self.move_up: pg_consts.K_UP,
                            self.move_down: pg_consts.K_DOWN,
                            self.move_left: pg_consts.K_LEFT,
                            self.move_right: pg_consts.K_RIGHT,}

    def moving(self):
        keys = pygame.key.get_pressed()

        if pressed_buttons := tuple(move_method
                                    for move_method, button_id in self._directions.items()
                                    if keys[button_id]):
            pressed_buttons[0]()

        else:
            self.stop(swap_sprite=True)



