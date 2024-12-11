import typing
from bisect import bisect
from bisect import bisect_left
from collections.abc import Callable
from itertools import cycle
from typing import Any

from functional import seq

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import sign
from aocl.p2 import P2

type Map = list[list[str]]


# for debugging purposes
@typing.no_type_check
def print_map(
    ndarray: Map,
    new_blockage: P2,
    starting_pos: P2,
    starting_dir: Callable,
    been_there: set[tuple[P2, Callable]],
    loop_pos: P2,
):
    def been(pos, dir):
        return (pos, dir) in been_there

    def above(pos):
        return been(p2.up(pos), p2.up) or been(p2.up(pos), p2.down) or been(pos, p2.down)

    def below(pos):
        return been(p2.down(pos), p2.up) or been(p2.down(pos), p2.down) or been(pos, p2.up)

    def left(pos):
        return been(p2.left(pos), p2.right) or been(p2.left(pos), p2.left) or been(pos, p2.right)

    def right(pos):
        return been(p2.right(pos), p2.right) or been(p2.right(pos), p2.left) or been(pos, p2.left)

    min_x, max_x, min_y, max_y = None, None, None, None
    for pos, _ in been_there:
        if min_x is None:
            min_x = max_x = pos[0]
            min_y = max_y = pos[1]
            continue
        min_x = min(min_x, pos[0])
        max_x = max(max_x, pos[0])
        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])

    shape = ndarray.shape
    min_x = max(min_x - 1, 0)
    max_x = min(max_x + 1, shape[0])
    min_y = max(min_y - 1, 0)
    max_y = min(max_y + 1, shape[1])

    output: list[str] = [""]

    for i in range(min_x, max_x + 1):
        line = []
        for j in range(min_y, max_y + 1):
            pos = (i, j)

            if new_blockage == pos:
                line.append("O")
            elif (ndarray[pos]) == "#":
                # print("𜺏", end="")
                line.append("🮘")
            elif starting_pos == pos:
                if starting_dir == p2.left:
                    line.append("<")
                elif starting_dir == p2.right:
                    line.append(">")
                elif starting_dir == p2.up:
                    line.append("^")
                else:
                    line.append("v")
            elif loop_pos == pos:
                line.append("🯆")
            elif above(pos) and below(pos) and left(pos) and right(pos):
                line.append("╋")
            elif below(pos) and left(pos) and right(pos):
                line.append("┳")
            elif above(pos) and left(pos) and right(pos):
                line.append("┻")
            elif above(pos) and below(pos) and left(pos):
                line.append("┫")
            elif above(pos) and below(pos) and right(pos):
                line.append("┣")
            elif below(pos) and left(pos):
                line.append("┓")
            elif below(pos) and right(pos):
                line.append("┏")
            elif above(pos) and left(pos):
                line.append("┛")
            elif above(pos) and right(pos):
                line.append("┗")
            elif left(pos) or right(pos):
                line.append("━")
            elif above(pos) or below(pos):
                line.append("┃")
            else:
                line.append(" ")
        output.append("".join(line))


def turn_right(dir: Callable) -> Callable:
    if dir == p2.right:
        return p2.down
    if dir == p2.down:
        return p2.left
    if dir == p2.left:
        return p2.up
    if dir == p2.up:
        return p2.right
    raise ValueError


type X = int
type Y = int


def move_up_to_blockage(
    pos: P2,
    direction: Callable,
    blockages_by_row: dict[X, list[Y]],
    blockages_by_col: dict[Y, list[X]],
    shape: p2.Shape,
) -> P2:
    row, col = pos

    next_row = row
    next_col = col
    match direction:
        case p2.left:
            if row in blockages_by_row:
                candidates = blockages_by_row[row]
                # -1 because we're going left
                # +1 because we move to the cell right to the blockage
                next_col = blockages_by_row[row][bisect(candidates, col) - 1] + 1
            else:
                next_col = -1  # moving out of bound
        case p2.right:
            if row in blockages_by_row:
                candidates = blockages_by_row[row]
                # -1 because we move to the cell left to the blockage
                next_col = blockages_by_row[row][bisect(candidates, col)] - 1
            else:
                next_col = shape[1]  # moving out of bound
        case p2.up:
            if col in blockages_by_col:
                candidates = blockages_by_col[col]
                # -1 because we're going up
                # +1 because we move to the cell below the blockage
                next_row = blockages_by_col[col][bisect(candidates, row) - 1] + 1
            else:
                next_row = -1  # moving out of bound
        case p2.down:
            if col in blockages_by_col:
                candidates = blockages_by_col[col]
                # -1 because we move to the cell above the blockage
                next_row = blockages_by_col[col][bisect(candidates, row)] - 1
            else:
                next_row = shape[0]  # moving out of bound
        case _:
            raise ValueError(f"Unknown direction: {direction=}")
    return (next_row, next_col)


def generate_blockages_dicts(lab: Map) -> tuple[dict[X, list[Y]], dict[Y, list[X]]]:
    shape = p2.shape(lab)
    blockages = p2.where_in_matrix(lab, "#")
    by_rows = (
        seq(blockages)
        .group_by_key()
        .starmap(lambda key, value: (key, sorted(value + [-2, shape[0] + 1])))
        .to_dict()
    )
    by_cols = (
        seq(blockages)
        .starmap(lambda x, y: (y, x))
        .group_by_key()
        .starmap(lambda key, value: (key, sorted(value + [-2, shape[1] + 1])))
        .to_dict()
    )
    return by_rows, by_cols


def generate_middle_points(start: P2, end: P2) -> list[P2]:
    # either ∆x or ∆y is going to be 0
    count = abs(end[0] - start[0] + end[1] - start[1]) + 1
    x_sign = sign(start[0], end[0])
    y_sign = sign(start[1], end[1])

    return [
        (
            start[0] + i * x_sign,
            start[1] + i * y_sign,
        )
        for i in range(count)
    ]


def clean_blockages(new_blockage: P2, blockages_by_row, blockages_by_col):
    blockage_x, blockage_y = new_blockage
    col_idx = bisect_left(blockages_by_row[blockage_x], blockage_y)
    del blockages_by_row[blockage_x][col_idx]
    if len(blockages_by_row[blockage_x]) == 0:
        # delete key from dict if list empty
        del blockages_by_row[blockage_x]
    row_idx = bisect_left(blockages_by_col[blockage_y], blockage_x)
    del blockages_by_col[blockage_y][row_idx]
    if len(blockages_by_col[blockage_y]) == 0:
        # delete key from dict if list empty
        del blockages_by_col[blockage_y]


def is_cycle(
    new_blockage: P2,
    blockages_by_row: dict[X, list[Y]],
    blockages_by_col: dict[Y, list[X]],
    starting_pos: P2,
    dir: Callable,
    shape: p2.Shape,
    ndarray: Map,
) -> bool:
    # prep work
    blockage_x, blockage_y = new_blockage
    if blockage_x not in blockages_by_row:
        blockages_by_row[blockage_x] = []
    if blockage_y not in blockages_by_col:
        blockages_by_col[blockage_y] = []
    blockages_by_row[blockage_x] = sorted(blockages_by_row[blockage_x] + [blockage_y])
    blockages_by_col[blockage_y] = sorted(blockages_by_col[blockage_y] + [blockage_x])

    result = is_cycle_subroutine(
        new_blockage, blockages_by_row, blockages_by_col, starting_pos, dir, shape
    )

    # cleanup
    clean_blockages(new_blockage, blockages_by_row, blockages_by_col)

    return result


def is_cycle_subroutine(
    new_blockage: P2,
    blockages_by_row: dict[X, list[Y]],
    blockages_by_col: dict[Y, list[X]],
    starting_pos: P2,
    dir: Callable,
    shape: p2.Shape,
):
    pos = starting_pos
    direction = dir
    been_there = set()

    while True:
        direction = turn_right(direction)
        next_pos = move_up_to_blockage(pos, direction, blockages_by_row, blockages_by_col, shape)
        if not p2.in_shape(next_pos, shape):
            return False
        for tmp_pos in generate_middle_points(pos, next_pos)[1:]:
            t = (tmp_pos, direction)
            if t in been_there:
                # print_map(ndarray, new_blockage, starting_pos, dir, been_there, tmp_pos)
                return True
            else:
                been_there.add(t)
        pos = next_pos
    return False


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Map:
        return input_data.as_list_of_lists

    @classmethod
    def process_part_one(cls, parsed_input: Map, **kwargs: Any) -> int:
        shape = p2.shape(parsed_input)
        start_pos: P2 = p2.where_in_matrix(parsed_input, "^")[0]
        directions = cycle([p2.up, p2.right, p2.down, p2.left])

        blockages_by_row, blockages_by_col = generate_blockages_dicts(parsed_input)

        pos = start_pos
        corners = [pos]

        while p2.in_shape(pos, shape):
            pos = move_up_to_blockage(
                pos, next(directions), blockages_by_row, blockages_by_col, shape
            )
            corners.append(pos)

        return (
            len(
                seq(corners)
                .zip(corners[1:])
                .starmap(lambda a, b: generate_middle_points(a, b))
                .flatten()
                .to_set()
            )
            - 1
        )  # remove one for the out of bound point

    @classmethod
    def process_part_two(cls, parsed_input: Map, **kwargs: Any) -> int:
        shape = p2.shape(parsed_input)

        start_pos: P2 = p2.where_in_matrix(parsed_input, "^")[0]
        been_there = set()
        been_there.add(start_pos)

        curr_pos: P2 = start_pos
        curr_dir = p2.up

        blockages = set()
        blockages_by_row, blockages_by_col = generate_blockages_dicts(parsed_input)

        while p2.in_shape(curr_pos, shape):
            next_dir = curr_dir
            next_pos = next_dir(curr_pos)
            if not p2.in_shape(next_pos, shape):
                break
            if parsed_input[next_pos[0]][next_pos[1]] == "#":
                next_dir = turn_right(curr_dir)
                next_pos = next_dir(curr_pos)

            # test if this would be a cycle
            if next_pos != start_pos and next_pos not in been_there:
                if is_cycle(
                    next_pos,
                    blockages_by_row,
                    blockages_by_col,
                    curr_pos,
                    curr_dir,
                    shape,
                    parsed_input,
                ):
                    blockages.add(next_pos)

            curr_pos = next_pos
            curr_dir = next_dir
            been_there.add(next_pos)

        return len(blockages)
