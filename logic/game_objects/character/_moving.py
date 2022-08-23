from enum import Enum

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
                pass

    def move_up(self):
        self._move(direction=_MoveDirection.Up)

    def move_down(self):
        self._move(direction=_MoveDirection.Down)

    def move_left(self):
        self._move(direction=_MoveDirection.Left)

    def move_right(self):
        self._move(direction=_MoveDirection.Right)

    def stop(self):
        self._move()
