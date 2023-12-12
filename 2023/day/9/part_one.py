import os
import re
import sys

from typing import Callable
from typing import Optional
from operator import sub

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from contextlib import suppress
from functional import seq
from functional.pipeline import Sequence
from loguru import logger

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")

TEST_INPUT_RESULT = 114
REAL_INPUT_RESULT = 1666172641


class PartZero(ABC):
    default_input = "./input"
    def __init__(self, filename: Optional[str]=None):
        self.input_name = filename or self.default_input
        self.input_path = filename or os.path.join(os.path.dirname(__file__), self.default_input)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.input_name}>"

    @property
    def as_str(self) -> list[str]:
        with open(self.input_path, "r") as f:
            return f.readlines()
    @property
    def as_iter(self) -> Iterable[str]:
        return iter(self.as_str)
    @property
    def as_seq(self) -> Sequence:
        return seq(self.as_str)

    @abstractmethod
    def process(self) -> int:
        ...

    def solve(self, expected: Optional[int]=None) -> bool:
        solution = self.process()
        if expected is None:
            logger.warning(f"{self!r} Found {solution:,d} ({solution}). No expected value provided.")
        elif expected == solution:
            logger.success(f"{self!r} Found {solution:,d} ({solution}).")
        else:
            logger.log("FAILED", f"{self!r} Found {solution:,d} != expected {expected:,d}.")
        return expected is not None and solution == expected

class PartOne(PartZero):
    def parse_line(self, line: str) -> Sequence:
        return seq(re.findall(r"-?\d+", line)).map(int)

    def process(self) -> int:
        return self.as_seq.map(self.parse_line).map(self.reduce).sum()

    @staticmethod
    def reduce(numbers: Sequence, index: int=-1, sign=1) -> int:
        if not any(numbers):
            return 0

        next_list = seq(zip(numbers, numbers[1:])).starmap(lambda x, y: y - x).to_list()
        return numbers[index] + sign * PartOne.reduce(next_list, index, sign)


class PartOneExample(PartOne):
    default_input = "./test_input"


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartOneExample().solve(TEST_INPUT_RESULT)
    PartOne(input).solve(REAL_INPUT_RESULT)

def test_test_input__part_one():
    assert PartOneExample().solve(TEST_INPUT_RESULT)

def test_real_input__part_one():
    assert PartOne().solve(REAL_INPUT_RESULT)

def test_reduce():
    assert PartOneExample.reduce([0, 3, 6, 9, 12, 15]) == 18
