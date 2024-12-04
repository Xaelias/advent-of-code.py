import re
from contextlib import suppress
from enum import Enum
from typing import Any

import regex

from aocl.base import AoCInput
from aocl.base import Base


def find_first_and_last_number(line: str) -> int:
    """Find first and last number in a string"""
    numbers = re.sub(r"\D+", "", line)
    first = numbers[0]
    last = numbers[-1]
    total = int(first + last)
    return total


class Numbers(Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
    seven = "7"
    eight = "8"
    nine = "9"


PATTERN = rf"[0-9]|{'|'.join(n.name for n in Numbers)}"


def find_first_and_last_number_spelled(line: str) -> int:
    numbers = regex.finditer(PATTERN, line, overlapped=True)
    first_m = next(numbers)
    try:
        *_, last_m = numbers
    except Exception:
        last_m = first_m

    first = first_m.group(0)
    last = last_m.group(0)

    with suppress(KeyError):
        first = Numbers[first].value
    with suppress(KeyError):
        last = Numbers[last].value

    return int(first + last)


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.as_list_of_str

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        return sum(map(find_first_and_last_number, parsed_input))

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        return sum(map(find_first_and_last_number_spelled, parsed_input))
