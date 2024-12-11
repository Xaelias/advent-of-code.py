from collections import Counter
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


def abs_diff(input: tuple[str, str]) -> int:
    return abs(int(input[1]) - int(input[0]))


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[str]]:
        return list(map(list, zip(*[l.split() for l in input_data.as_list_of_str])))  # noqa: E741

    @classmethod
    def process_part_one(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
        left = sorted(parsed_input[0])
        right = sorted(parsed_input[1])

        return sum(map(abs_diff, zip(left, right)))

    @classmethod
    def process_part_two(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
        left = [int(s) for s in parsed_input[0]]
        right = [int(s) for s in parsed_input[1]]
        left_count: dict[int, int] = Counter(left)
        right_count: dict[int, int] = Counter(right)

        total = 0
        for k in left_count:
            if k in right:
                total += k * left_count[k] * right_count[k]
        return total
