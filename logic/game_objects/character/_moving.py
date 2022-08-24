from enum import Enum

import pygame
from pygame.surface import Surface

from logic.game_objects.character._map_position import _MapPosition, Position


class _MoveDirection(Enum):
    Left = 'left'
    Right = 'right'
    Up = 'up'
    Down = 'down'


class _Moving(_MapPosition):
    """
        Класс для перемещения персонажа
    """
    frames_for_walk: list[Surface] = None
    current_frame_for_walk: Surface = None

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
            case _:
                self.next_position = Position(0, 0)

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
                if not self.frames_for_walk:
                    self.frames_for_walk = [self.action_back,] * 4 + \
                                           [pygame.transform.flip(self.action_back, True, False),] * 4

                self.image = self.frames_for_walk.pop(0)

            case _MoveDirection.Down:
                if not self.frames_for_walk:
                    self.frames_for_walk = [self.action_front_walk_0,] * 4 + \
                                           [self.action_front_walk_1,] * 4
                self.image = self.frames_for_walk.pop(0)

            case _MoveDirection.Right | _MoveDirection.Left:
                if not self.frames_for_walk:
                    self.frames_for_walk = [self.action_walk_0,
                                            self.action_walk_1,
                                            self.action_walk_2,
                                            self.action_walk_3,
                                            self.action_walk_4,
                                            self.action_walk_5,
                                            self.action_walk_6,
                                            self.action_walk_7,
                                            ]

                new_image = self.frames_for_walk.pop(0)

                if direction == _MoveDirection.Left:
                    new_image = pygame.transform.flip(new_image, True, False)

                self.image = new_image

            # case _:
            #     self.image = self.action_side

    def stop(self):
        self._move()
