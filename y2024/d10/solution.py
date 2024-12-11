from operator import itemgetter
from typing import Any

from functional import seq
from numpy.typing import NDArray

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def find_trails(cls, topographic_map: NDArray) -> list[tuple[p2.P2, p2.P2]]:
        trailheads = p2.where_in_ndarray(topographic_map, 0)

        stack = [(trailhead, 0, trailhead) for trailhead in trailheads]
        valid = []

        while stack:
            (start, value, pos), *stack = stack

            if value == 9:
                valid.append((start, pos))
                continue

            for neighbor in p2.neighbors(pos, topographic_map.shape):
                if topographic_map[*neighbor] == value + 1:
                    stack.append((start, value + 1, neighbor))

        return valid

    @classmethod
    def parse(cls, input_data: AoCInput) -> list[tuple[p2.P2, p2.P2]]:
        ndarray = input_data.as_nparray
        ndarray[ndarray == "."] = "-1"
        return cls.find_trails(ndarray.astype(int))

    @classmethod
    def process_part_one(cls, parsed_input: list[tuple[p2.P2, p2.P2]], **kwargs: Any) -> int:
        return seq(set(parsed_input)).group_by_key().map(itemgetter(1)).map(len).sum()

    @classmethod
    def process_part_two(cls, parsed_input: list[tuple[p2.P2, p2.P2]], **kwargs: Any) -> int:
        return seq(parsed_input).group_by_key().map(itemgetter(1)).map(len).sum()
