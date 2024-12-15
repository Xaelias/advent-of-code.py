import itertools
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> str:
        return input_data.raw

    @classmethod
    def process_part_one(cls, parsed_input: str, **kwargs: Any) -> int:
        iterations = int(kwargs.get("iterations", 40))

        line = parsed_input
        for i in range(iterations):
            line = "".join(
                [f"{len([_ for _ in seq])}{char}" for char, seq in itertools.groupby(line)]
            )
        return len(line)

    @classmethod
    def process_part_two(cls, parsed_input: str, **kwargs: Any) -> int:
        return cls.process_part_one(parsed_input, iterations=50)
