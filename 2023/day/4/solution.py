import re
from typing import Any

from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base


# Card #: winning #      | numbers you have
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
def process_line(line: str) -> set[int]:
    winning, numbers = line.split(": ")[1].split(" | ")
    winning_set = set(map(int, re.findall(r"\d+", winning)))
    numbers_set = set(map(int, re.findall(r"\d+", numbers)))

    return numbers_set & winning_set


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return list(map(process_line, input_data.as_list_of_str))

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        return sum(map(lambda common: int(2 ** (len(common) - 1)), parsed_input))

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        to_add: list[tuple[int, int]] = []
        points = 0
        for common in parsed_input:
            count = 1 + sum((count for count, _ in to_add))
            points += count
            logger.debug(f"Running score: {points}. [{to_add=}, {count=}]")
            to_add = [(count, for_next - 1) for count, for_next in to_add if for_next > 1]
            if common:
                to_add.append((count, len(common)))
        return points
