from enum import IntEnum


class MoveDirection(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3
    Stop = 4


class DirectionsConsts:
    AllDirections = (MoveDirection.Up,
                     MoveDirection.Down,
                     MoveDirection.Left,
                     MoveDirection.Right)
    NoWay = ()
    ToLeft = (MoveDirection.Left,)
    ToRight = (MoveDirection.Right,)
    ToUp = (MoveDirection.Up,)
    ToDown = (MoveDirection.Down,)

    XMoving = (MoveDirection.Left,
               MoveDirection.Right)
    YMoving = (MoveDirection.Up,
               MoveDirection.Down)
