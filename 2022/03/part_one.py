import os
import sys

from typing import Callable
from typing import Optional

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from contextlib import suppress
from functional import seq
from functional.pipeline import Sequence
from loguru import logger

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")

TEST_INPUT_RESULT = 157
REAL_INPUT_RESULT = 7997


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
    def parse_line(self, line: str) -> str:
        n = len(line) // 2
        return set(line[:n]).intersection(set(line[n:])).pop()

    def map_letter_to_score(self, letter: str) -> int:
        if letter.islower():
            return ord(letter) - ord("a") + 1
        return ord(letter) - ord("A") + 27

    def process(self) -> int:
        return self.as_seq.map(str.strip).map(self.parse_line).map(self.map_letter_to_score).sum()

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
