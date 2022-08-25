from enum import IntEnum


class ActionType(IntEnum):
    """
        Все действия делаются СЛЕВА НА ПРАВО
    """
    usual = 0

    lifting_up = 1
    lifting_down = 2
