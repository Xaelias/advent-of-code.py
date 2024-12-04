from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return list(map(sum, [map(int, chunk) for chunk in input_data.as_chunks]))

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        return max(parsed_input)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        return sum(sorted(parsed_input)[-3:])
