from dataclasses import dataclass


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
