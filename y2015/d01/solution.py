from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[str]:
        return list(input_data.raw)

    @classmethod
    def process_part_one(cls, parsed_input: list[str], **kwargs: Any) -> int:
        return sum([1 if c == "(" else -1 for c in parsed_input])

    @classmethod
    def process_part_two(cls, parsed_input: list[str], **kwargs: Any) -> int:
        total = 0
        for idx, c in enumerate(parsed_input):
            total += 1 if c == "(" else -1
            if total < 0:
                break
        return idx + 1
