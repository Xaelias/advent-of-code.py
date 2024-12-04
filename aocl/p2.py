from collections.abc import Callable
from collections.abc import Iterable
from functools import cache

RULD = [(0, 1), (-1, 0), (0, -1), (1, 0)]

P2 = tuple[int, int]
Matrix = list[list[int | str | bool]]
StrMatrix = list[list[str]]
IntMatrix = list[list[int]]
BoolMatrix = list[list[bool]]
Shape = tuple[int, int]


def in_shape(position: P2, shape: Shape) -> bool:
    return 0 <= position[0] < shape[0] and 0 <= position[1] < shape[1]


def adj(position: P2, shape: Shape | None) -> Iterable[P2]:
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


all_eight_directions_functions = [
    right,
    up_right,
    up,
    up_left,
    left,
    down_left,
    down,
    down_right,
]

all_four_directions_functions = [
    right,
    up,
    left,
    down,
]


def go_direction(position: P2, direction: str, times: int):
    offset = RULD["RULD".index(direction)]
    return position[0] + times * offset[0], position[1] + times * offset[1]


def get_points_in_direction(
    nparray,
    start: P2,
    direction: Callable[[P2], P2],
    count: int,
    stay_in_shape: bool = True,
) -> str:
    result = []
    shape = nparray.shape
    pos = start
    if in_shape(pos, shape) or not stay_in_shape:
        result.append(nparray[pos])
        for _ in range(count - 1):
            pos = direction(pos)
            if in_shape(pos, shape) or not stay_in_shape:
                result.append(nparray[pos])
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
