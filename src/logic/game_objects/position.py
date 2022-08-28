from dataclasses import dataclass
from enum import IntEnum

from src.logic.game_objects.character.mechanics.action import ActionType


class MoveDirection(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3
    Stop = 4


@dataclass
class Position:
    x: int
    y: int


class _MapPosition:
    """
        Класс реализующий интерфейс нахождения персонажа на карте, его координаты на ней
    """
    _one_step: int = None
    _spawn_point: Position = None
    _position: Position = None
    _next_position: Position = None
    _step_up: int = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Position):
        self._position = value

    @property
    def next_position(self):
        return self._next_position

    @next_position.setter
    def next_position(self, value: Position):
        self._next_position = value

    @property
    def spawn_point(self):
        return self._spawn_point

    @spawn_point.setter
    def spawn_point(self, value):
        self.next_position = self._spawn_point = value

    @property
    def one_step(self):
        return self._one_step

    @one_step.setter
    def one_step(self, value):
        if not isinstance(value, int):
            raise TypeError('"Step up" должен быть "Int"')
        self._one_step = value
        self.step_up = int(self.one_step / 2)

    @property
    def step_up(self):
        return self._step_up

    @step_up.setter
    def step_up(self, value):
        if not isinstance(value, int):
            raise TypeError('"Step up" должен быть "Int"')
        self._step_up = value

    def get_next_position_up(self):
        return self._next_position.y - self.one_step

    def position_up(self):
        self._next_position.y -= self.one_step

    def get_next_position_down(self):
        return self._next_position.y + self.one_step

    def position_down(self):
        self._next_position.y += self.one_step

    def get_next_position_left(self):
        return self._next_position.x - self.one_step

    def position_left(self):
        self._next_position.x -= self.one_step

    def get_next_position_right(self):
        return self._next_position.x + self.one_step

    def position_right(self):
        self._next_position.x += self.one_step

    def position_stop(self):
        self._next_position = Position(0, 0)

    def position_lifting(self,
                         direction: MoveDirection,
                         action_type: ActionType):
        multiplier = -1 if direction == MoveDirection.Left else 1

        match action_type:

            case ActionType.lifting_up:
                # подъём - вправо , спуск - влево
                self.next_position.y -= self.step_up * multiplier

            case ActionType.lifting_down:
                # спуск - вправо, подъём - влево
                self.next_position.y += self.step_up * multiplier



