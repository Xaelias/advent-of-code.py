from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.raw.strip()

    @classmethod
    def process_part_one(cls, parsed_input: Any, prefix_size: int = 4, **kwargs: Any) -> int | str:
        for i in range(len(parsed_input) - (prefix_size - 1)):
            substring = parsed_input[i : i + prefix_size]
            if len(set(substring)) == prefix_size:
                return i + prefix_size
        raise ValueError(
            f"Could not find solution for {parsed_input!r} with prefix size of {prefix_size}."
        )

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        return cls.process_part_one(parsed_input, prefix_size=14, **kwargs)
