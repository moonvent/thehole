from enum import Enum
from typing import NamedTuple


class Files(Enum):
    ...


class Folders(Enum):
    Static = 'static'
    Characters = 'characters'


class _GameConstant:
    """
        Константы используемые для игры, размеры экрана, сложность, и т.д.
    """

    class _Size(NamedTuple):
        width: int
        height: int

    Size = _Size(800, 600)

    _amount_fps: int = 60

    @property
    def AmountFps(self):
        return self._amount_fps

    _title = 'Adventure'

    @property
    def Title(self):
        return self._title

    _default_skin_folder: str = 'Male adventurer'

    @property
    def DefaulSkinFolder(self):
        return self._default_skin_folder


GameConstants = _GameConstant()
