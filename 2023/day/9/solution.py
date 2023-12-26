import re
from typing import Any

from functional import seq
from functional.pipeline import Sequence

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        def parse_line(line: str) -> Sequence:
            return seq(re.findall(r"-?\d+", line)).map(int)

        return input_data.as_seq.map(parse_line)

    @staticmethod
    def reduce(numbers: Sequence, index: int = -1, sign=1) -> int:
        if not any(numbers):
            return 0

        next_list = seq(zip(numbers, numbers[1:])).starmap(lambda x, y: y - x).to_list()
        return numbers[index] + sign * Solution.reduce(next_list, index, sign)

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        return parsed_input.map(Solution.reduce).sum()

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        return parsed_input.map(lambda x: Solution.reduce(x, index=0, sign=-1)).sum()
