from typing import Any
from typing import Callable

from functional import seq
from numpy.typing import NDArray

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base


def is_xmas(nparray: NDArray, starting_pos: p2.P2, dir_fn: Callable[[p2.P2], p2.P2]) -> bool:
    return (
        p2.get_points_in_direction(
            nparray,
            starting_pos,
            dir_fn,
            count=4,
        )
        == "XMAS"
    )


def is_x_mas(nparray: NDArray, a_pos: p2.P2) -> bool:
    up_left = p2.up_left(a_pos)
    down_left = p2.down_left(a_pos)
    return p2.get_points_in_direction(
        nparray,
        up_left,
        p2.down_right,
        count=3,
    ) in ("MAS", "SAM") and p2.get_points_in_direction(
        nparray,
        down_left,
        p2.up_right,
        count=3,
    ) in ("MAS", "SAM")


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[str]]:
        return input_data.as_nparray

    @classmethod
    def process_part_one(cls, parsed_input: NDArray, **kwargs: Any) -> int:
        exes = p2.where_in_ndarray(parsed_input, "X")
        return (
            seq(exes)
            .cartesian(p2.all_eight_directions_functions)
            .starmap(lambda starting_pos, dir_fn: is_xmas(parsed_input, starting_pos, dir_fn))
            .sum()
        )

    @classmethod
    def process_part_two(cls, parsed_input: NDArray, **kwargs: Any) -> int:
        aces = p2.where_in_ndarray(parsed_input, "A")
        return seq(aces).map(lambda a_pos: is_x_mas(parsed_input, a_pos)).sum()

    # @classmethod
    # def process_part_one(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
    #     exes = zip(*np.where(parsed_input == "X"))

    #     total = 0
    #     for ex in exes:
    #         for direction in p2.all_eight_directions_functions:
    #             total += p2.get_points_in_direction(parsed_input, ex, direction, count=4) == "XMAS"
    #     return total

    # @classmethod
    # def process_part_two(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
    #     aces = zip(*np.where(parsed_input == "A"))

    #     total = 0
    #     for ass in aces:
    #         up_left = p2.up_left(ass)
    #         down_left = p2.down_left(ass)

    #         total += p2.get_points_in_direction(
    #             parsed_input,
    #             up_left,
    #             p2.down_right,
    #             count=3,
    #         ) in ("MAS", "SAM") and p2.get_points_in_direction(
    #             parsed_input,
    #             down_left,
    #             p2.up_right,
    #             count=3,
    #         ) in ("MAS", "SAM")

    #     return total
