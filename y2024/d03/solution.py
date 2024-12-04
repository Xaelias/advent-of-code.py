from typing import Any

import regex
from functional import seq

from aocl.base import AoCInput
from aocl.base import Base

MUL_PATTERN = r"mul\((\d{1,3}),(\d{1,3})\)"
DO = "do()"
DONT = "don't()"


def process_mul(mul: tuple[str, str]) -> int:
    return int(mul[0]) * int(mul[1])


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> str:
        return input_data.raw

    @classmethod
    def process_part_one(cls, parsed_input: str, **kwargs: Any) -> int:
        # return sum(map(process_mul, map(regex.Match.groups, regex.finditer(MUL_PATTERN, parsed_input))))
        return (
            seq(regex.finditer(MUL_PATTERN, parsed_input))
            .map(regex.Match.groups)
            .map(process_mul)
            .sum()
        )

    @classmethod
    def process_part_two(cls, parsed_input: str, **kwargs: Any) -> int:
        # return sum(map(cls.process_part_one, map(lambda x: x.split(DONT, maxsplit=1)[0], parsed_input.split(DO))))
        return (
            seq(parsed_input.split(DO))
            .map(lambda x: x.partition(DONT)[0])
            .map(cls.process_part_one)
            .sum()
        )
