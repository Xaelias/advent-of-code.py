from typing import Any
from typing import Callable

from functional import seq

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base


def get_points_in_direction(
    matrix: p2.StrMatrix,
    start: p2.P2,
    direction: Callable[[p2.P2], p2.P2],
    count: int,
    stay_in_shape: bool = True,
) -> str:
    result = []
    shape = p2.shape(matrix)
    pos = start
    if p2.in_shape(pos, shape) or not stay_in_shape:
        result.append(p2.matrix_get(matrix, pos))
        for _ in range(count - 1):
            pos = direction(pos)
            if p2.in_shape(pos, shape) or not stay_in_shape:
                result.append(p2.matrix_get(matrix, pos))
            else:
                break
    return "".join(result)


def is_xmas(nparray: p2.StrMatrix, starting_pos: p2.P2, dir_fn: Callable[[p2.P2], p2.P2]) -> bool:
    return (
        get_points_in_direction(
            nparray,
            starting_pos,
            dir_fn,
            count=4,
        )
        == "XMAS"
    )


def is_x_mas(nparray: p2.StrMatrix, a_pos: p2.P2) -> bool:
    up_left = p2.up_left(a_pos)
    down_left = p2.down_left(a_pos)
    return get_points_in_direction(
        nparray,
        up_left,
        p2.down_right,
        count=3,
    ) in ("MAS", "SAM") and get_points_in_direction(
        nparray,
        down_left,
        p2.up_right,
        count=3,
    ) in ("MAS", "SAM")


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[str]]:
        return input_data.as_list_of_lists

    @classmethod
    def process_part_one(cls, parsed_input: p2.StrMatrix, **kwargs: Any) -> int:
        exes = p2.where_in_matrix(parsed_input, "X")
        return (
            seq(exes)
            .cartesian(p2.all_eight_directions_functions)
            .starmap(lambda starting_pos, dir_fn: is_xmas(parsed_input, starting_pos, dir_fn))
            .sum()
        )

    @classmethod
    def process_part_two(cls, parsed_input: p2.StrMatrix, **kwargs: Any) -> int:
        aces = p2.where_in_matrix(parsed_input, "A")
        return seq(aces).map(lambda a_pos: is_x_mas(parsed_input, a_pos)).sum()

    # @classmethod
    # def process_part_one(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
    #     exes = zip(*np.where(parsed_input == "X"))

    #     total = 0
    #     for ex in exes:
    #         for direction in p2.all_eight_directions_functions:
    #             total += get_points_in_direction(parsed_input, ex, direction, count=4) == "XMAS"
    #     return total

    # @classmethod
    # def process_part_two(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
    #     aces = zip(*np.where(parsed_input == "A"))

    #     total = 0
    #     for ass in aces:
    #         up_left = p2.up_left(ass)
    #         down_left = p2.down_left(ass)

    #         total += get_points_in_direction(
    #             parsed_input,
    #             up_left,
    #             p2.down_right,
    #             count=3,
    #         ) in ("MAS", "SAM") and get_points_in_direction(
    #             parsed_input,
    #             down_left,
    #             p2.up_right,
    #             count=3,
    #         ) in ("MAS", "SAM")

    #     return total
