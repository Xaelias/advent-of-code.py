from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[int]]:
        return [[int(e) for e in line.split("x")] for line in input_data.as_lines]

    @classmethod
    def process_part_one(cls, parsed_input: list[list[int]], **kwargs: Any) -> int:
        return sum(
            [
                2 * (l * w + w * h + h * l) + (l * w * h) // max(l, w, h)
                for (l, w, h) in parsed_input  # noqa: E741
            ]
        )

    @classmethod
    def process_part_two(cls, parsed_input: list[list[int]], **kwargs: Any) -> int:
        return sum([(l * w * h) + 2 * (l + w + h - max(l, w, h)) for (l, w, h) in parsed_input])  # noqa: E741
