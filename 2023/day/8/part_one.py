import os
import re
import sys

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from contextlib import suppress
from functional import seq
from loguru import logger
from typing import Optional

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")

TEST_INPUT_RESULT = 2
REAL_INPUT_RESULT = 18827


class Main(ABC):
    default_input = "./input"
    def __init__(self, input: Optional[str]=None):
         self.input = input or os.path.join(os.path.dirname(__file__), self.default_input)

    def str(self) -> list[str]:
        with open(self.input, "r") as f:
            return f.readlines()

    def iter(self) -> Iterable[str]:
        return iter(self.str())

    @abstractmethod
    def parse(self):
        ...

    @abstractmethod
    def process(self) -> int:
        ...

    def solve(self, expected: Optional[int]=None) -> bool:
        solution = self.process()
        if expected is not None:
            if solution == expected:
                logger.success(f"Solution for {self.__class__.__name__}: {solution:,d} ({solution}).")
            else:
                logger.log("FAILED", f"Expected solution for {self.__class__.__name__} to be {expected:,d} but found {solution:,d}.")
        else:
            logger.warning(f"Solution for {self.__class__.__name__}: {solution:,d} ({solution}). No expected value provided.")
        return solution == expected

class Map:
    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"<Map: {self.name} L={self.left} R={self.right}>"

    @classmethod
    def convert(cls, line: str) -> "Map":
        return cls(line[0:3], line[7:10], line[12:15])

    def next(self, direction: str) -> str:
        return self.left if direction == "L" else self.right

class PartOne(Main):
    def parse(self) -> "???":
        s = self.str()
        directions = s[0].strip()
        maps = seq(s[2:]).map(Map.convert).map(lambda m: (m.name, m)).dict()
        return directions, maps

    def process(self, start: Optional[str]="AAA", end="Z") -> int:
        directions, maps = self.parse()

        i = -1
        current = maps[start]
        while not current.name.endswith(end):
            i += 1
            direction = directions[i % len(directions)]
            current = maps[current.next(direction)]
        return i + 1


class PartOneExample(PartOne):
    default_input = "./test_input"

class PartOneExampleTwo(PartOne):
    default_input = "./test_input_2"

if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartOneExample().solve(TEST_INPUT_RESULT)
    PartOneExampleTwo().solve(6)
    PartOne(input).solve(REAL_INPUT_RESULT)

def test_test_input():
    assert PartOneExample().solve(TEST_INPUT_RESULT)
    assert PartOneExampleTwo().solve(6)

def test_input():
    assert PartOne().solve(REAL_INPUT_RESULT)
