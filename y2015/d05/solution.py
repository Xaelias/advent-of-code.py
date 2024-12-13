from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[str]:
        return input_data.as_lines

    @classmethod
    def is_nice_string_part_one(cls, line: list[str]) -> bool:
        vowels = 0
        double_letter = False
        bad_strings = False
        prev = curr = None
        while not bad_strings and line:
            prev = curr
            curr, *line = line

            vowels += curr in "aeiou"
            double_letter |= prev == curr

            bad_strings |= f"{prev}{curr}" in ("ab", "cd", "pq", "xy")
        return vowels >= 3 and double_letter and not bad_strings

    @classmethod
    def process_part_one(cls, parsed_input: list[str], **kwargs: Any) -> int:
        return sum((cls.is_nice_string_part_one(list(line)) for line in parsed_input))

    @classmethod
    def is_nice_string_part_two(cls, line: list[str]) -> bool:
        pairs = set()
        double_pairs = False
        repeat = False
        prev_prev_prev = prev_prev = prev = curr = None
        while line and not (double_pairs and repeat):
            prev_prev_prev, prev_prev, prev = prev_prev, prev, curr
            curr, *line = line

            prev_pair = f"{prev_prev_prev}{prev_prev}"
            mid_pair = f"{prev_prev}{prev}"
            pair = f"{prev}{curr}"
            if (pair in pairs and (mid_pair != pair or prev_pair == pair)) or double_pairs:
                double_pairs = True
            else:
                pairs.add(pair)

            repeat |= prev_prev == curr

        return double_pairs and repeat

    @classmethod
    def process_part_two(cls, parsed_input: list[str], **kwargs: Any) -> int:
        return sum((cls.is_nice_string_part_two(list(line)) for line in parsed_input))
