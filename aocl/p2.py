from collections.abc import Callable
from functools import cache
from typing import Any

import numpy as np
import numpy.lib.mixins
import numpy.typing as npt

RULD = [(0, 1), (-1, 0), (0, -1), (1, 0)]

type Matrix = list[list[Any]]
type StrMatrix = list[list[str]]
type IntMatrix = list[list[int]]
type BoolMatrix = list[list[bool]]
type Shape = tuple[int, ...]
type P2 = tuple[int, int]


def add(left: P2, right: P2) -> P2:
    return (left[0] + right[0], left[1] + right[1])


def sub(left: P2, right: P2) -> P2:
    return (left[0] - right[0], left[1] - right[1])


def in_shape(position: P2, shape: Shape) -> bool:
    return 0 <= position[0] < shape[0] and 0 <= position[1] < shape[1]


def right(position: P2) -> P2:
    return position[0], position[1] + 1


def up_right(position: P2) -> P2:
    return position[0] - 1, position[1] + 1


def up(position: P2) -> P2:
    return position[0] - 1, position[1]


def up_left(position: P2) -> P2:
    return position[0] - 1, position[1] - 1


def left(position: P2) -> P2:
    return position[0], position[1] - 1


def down_left(position: P2) -> P2:
    return position[0] + 1, position[1] - 1


def down(position: P2) -> P2:
    return position[0] + 1, position[1]


def down_right(position: P2) -> P2:
    return position[0] + 1, position[1] + 1


def neighbors(position: P2, shape: Shape | None = None) -> list[P2]:
    neighbors = [
        (position[0], position[1] + 1),  # R
        (position[0] + 1, position[1]),  # D
        (position[0], position[1] - 1),  # L
        (position[0] - 1, position[1]),  # U
    ]
    if shape is None:
        return neighbors
    return [e for e in neighbors if in_shape(e, shape)]


def all_neighbors(position: P2, shape: Shape | None = None) -> list[P2]:
    neighbors = [
        (position[0], position[1] + 1),  # R
        (position[0] + 1, position[1] + 1),  # DR
        (position[0] + 1, position[1]),  # D
        (position[0] + 1, position[1] - 1),  # DL
        (position[0], position[1] - 1),  # L
        (position[0] - 1, position[1] - 1),  # UL
        (position[0] - 1, position[1]),  # U
        (position[0] - 1, position[1] + 1),  # UR
    ]
    if shape is None:
        return neighbors
    return [e for e in neighbors if in_shape(e, shape)]


all_eight_directions_functions = [
    right,
    down_right,
    down,
    down_left,
    left,
    up_left,
    up,
    up_right,
]

all_four_directions_functions = [
    right,
    down,
    left,
    up,
]


def get_points_in_direction(
    nparray: npt.NDArray,
    start: P2,
    direction: Callable[[P2], P2],
    count: int,
    stay_in_shape: bool = True,
) -> str:
    result = []
    shape = nparray.shape
    pos = start
    if in_shape(pos, shape) or not stay_in_shape:
        result.append(nparray[*pos])
        for _ in range(count - 1):
            pos = direction(pos)
            if in_shape(pos, shape) or not stay_in_shape:
                result.append(nparray[*pos])
            else:
                break
    return "".join(result)


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


def rotate_matrix_left(matrix):
    outer_type = type(matrix)
    inner_type = type(matrix[0])

    zipped = zip(*matrix)

    if isinstance(matrix[0], str):
        zipped = map("".join, zipped)

    return outer_type(map(inner_type, zipped))[::-1]


def rotate_matrix_right(matrix):
    outer_type = type(matrix)
    inner_type = type(matrix[0])

    zipped = zip(*matrix[::-1])

    if isinstance(matrix[0], str):
        zipped = map("".join, zipped)

    return outer_type(map(inner_type, zipped))


def where_in_ndarray(ndarray: npt.NDArray, match: Any) -> list[P2]:
    return list(zip(*np.where(ndarray == match)))


def where_in_matrix(matrix: Matrix, match: Any) -> list[P2]:
    rows, cols = shape(matrix)
    return [(i, j) for i in range(rows) for j in range(cols) if matrix[i][j] == match]


def shape(matrix: Matrix) -> Shape:
    return (len(matrix), len(matrix[0]))
