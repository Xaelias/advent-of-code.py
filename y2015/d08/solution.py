import json
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[str]:
        return input_data.as_lines

    @classmethod
    def process_part_one(cls, parsed_input: list[str], **kwargs: Any) -> int:
        return sum(
            [
                len(line) - len(bytes(line, "utf-8").decode("unicode_escape")) + 2
                for line in parsed_input
            ]
        )

    @classmethod
    def process_part_two(cls, parsed_input: list[str], **kwargs: Any) -> int:
        return sum([len(json.dumps(line)) - len(line) for line in parsed_input])
