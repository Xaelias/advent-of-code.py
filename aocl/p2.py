from functools import cache
from typing import Iterable

RULD = [(0, 1), (-1, 0), (0, -1), (1, 0)]

P2 = tuple[int, int]
Shape = tuple[int, int]


def in_shape(position: P2, shape: Shape) -> bool:
    return 0 <= position[0] < shape[0] and 0 <= position[1] < shape[1]


def adj(position: P2, shape: Shape) -> Iterable[P2]:
    neighbors = [
        (position[0], position[1] + 1),  # R
        (position[0] + 1, position[1]),  # D
        (position[0], position[1] - 1),  # L
        (position[0] - 1, position[1]),  # U
    ]
    if shape is None:
        return neighbors
    return [e for e in neighbors if in_shape(e, shape)]


def right(position: P2) -> P2:
    return position[0], position[1] + 1


def up(position: P2) -> P2:
    return position[0] - 1, position[1]


def left(position: P2) -> P2:
    return position[0], position[1] - 1


def down(position: P2) -> P2:
    return position[0] + 1, position[1]


def go_direction(position: P2, direction: str, times: int):
    offset = RULD["RULD".index(direction)]
    return position[0] + times * offset[0], position[1] + times * offset[1]


@cache
def segments_cross(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    xx1: int,
    yy1: int,
    xx2: int,
    yy2: int,
) -> bool:
    x_seg = (min(x1, x2), max(x1, x2))
    y_seg = (min(y1, y2), max(y1, y2))

    xx_seg = (min(xx1, xx2), max(xx1, xx2))
    yy_seg = (min(yy1, yy2), max(yy1, yy2))

    return (
        x_seg[0] <= xx_seg[1]
        and xx_seg[0] <= x_seg[1]
        and y_seg[0] <= yy_seg[1]
        and yy_seg[0] <= y_seg[1]
    )
