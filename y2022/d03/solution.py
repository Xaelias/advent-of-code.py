from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


def score_letter(letter: str) -> int:
    n = ord(letter)
    a = ord("a")  # 97
    A = ord("A")  # 65
    if n < a:
        return n - A + 27
    return n - a + 1


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.as_list_of_str

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        total = 0
        for row in parsed_input:
            n = len(row) // 2
            first = set(row[:n])
            second = set(row[n:])
            total += score_letter((first & second).pop())
        return total

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        bags = map(set, parsed_input)  # noqa
        total = 0
        for first, second, third in zip(bags, bags, bags):
            total += score_letter((first & second & third).pop())
        return total
