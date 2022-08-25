from enum import Enum
from typing import NamedTuple

import pygame
from pygame.surface import Surface

from logic.game_objects.action import ActionType
from logic.game_objects.position import _MapPosition, Position
import pygame.locals as pg_consts


class MoveDirection(Enum):
    Left = 'left'
    Right = 'right'
    Up = 'up'
    Down = 'down'
    Stop = 'stop'


class _Moving(_MapPosition):
    """
        Класс для перемещения персонажа
    """
    _current_direction: MoveDirection = None
    _last_move_direction: MoveDirection = None
    _frames_for_walk: list[Surface] = None

    @property
    def direction(self):
        return self._current_direction

    @direction.setter
    def direction(self, new_direction: MoveDirection):
        self._current_direction = new_direction

    def _move(self,
              action_type: ActionType,
              direction: MoveDirection):

        match direction:
            case MoveDirection.Up:
                self.next_position.y -= self._one_step
                self.direction = MoveDirection.Up

            case MoveDirection.Down:
                self.next_position.y += self._one_step
                self.direction = MoveDirection.Down

            case MoveDirection.Left:

                match action_type:
                    case ActionType.lifting_up:
                        self.next_position.y += self._one_step / 2
                    case ActionType.lifting_down:
                        self.next_position.y -= self._one_step / 2

                self.next_position.x -= self._one_step
                self.direction = MoveDirection.Left

            case MoveDirection.Right:

                match action_type:
                    case ActionType.lifting_up:
                        self.next_position.y -= self._one_step / 2
                    case ActionType.lifting_down:
                        self.next_position.y += self._one_step / 2

                self.next_position.x += + self._one_step
                self.direction = MoveDirection.Right

            case MoveDirection.Stop:
                self.next_position = Position(0, 0)

            case _:
                self.next_position = Position(0, 0)
                return

        self.move_image(direction=direction)

    def move_up(self, action_type: ActionType):
        self._move(direction=MoveDirection.Up,
                   action_type=action_type)

    def move_down(self, action_type: ActionType):
        self._move(direction=MoveDirection.Down,
                   action_type=action_type)

    def move_left(self, action_type: ActionType):
        self._move(direction=MoveDirection.Left,
                   action_type=action_type)

    def move_right(self, action_type: ActionType):
        self._move(direction=MoveDirection.Right,
                   action_type=action_type)

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

    def stop(self,  action_type: ActionType, swap_sprite: bool = True):
        self._move(direction=MoveDirection.Stop if swap_sprite else None,
                   action_type=action_type)


class PlayerMovingMixin(_Moving):

    _directions: dict = None

    def __init__(self):
        self._directions = {self.move_up: pg_consts.K_UP,
                            self.move_down: pg_consts.K_DOWN,
                            self.move_left: pg_consts.K_LEFT,
                            self.move_right: pg_consts.K_RIGHT,}

    def moving(self, action_type: ActionType):
        keys = pygame.key.get_pressed()

        if pressed_buttons := tuple(move_method
                                    for move_method, button_id in self._directions.items()
                                    if keys[button_id]):
            pressed_buttons[0](action_type=action_type)

        else:
            self.stop(swap_sprite=True,
                      action_type=action_type)



