import os
import sys

from typing import Any
from typing import Callable
from typing import Optional

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from contextlib import suppress
from functools import partial
from functional import seq
from functional.pipeline import Sequence
from itertools import combinations
from loguru import logger

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")

class Input:
    def __init__(self, file_name: str):
        if os.path.exists(file_name):
            self.file_path = file_name
        elif os.path.exists(file_path := os.path.join(os.path.dirname(__file__), file_name)):
            self.file_path = file_path
        assert hasattr(self, "file_path")

        self.file_name = os.path.basename(self.file_path)

    @property
    def as_str(self) -> list[str]:
        with open(self.file_path, "r") as f:
            return f.readlines()
    @property
    def as_iter(self) -> Iterable[str]:
        return iter(self.as_str)
    @property
    def as_seq(self) -> Sequence:
        return seq(self.as_str)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.file_name}>"

class Prompt:
    def __init__(self, input: Input, expected: int, **kwargs: Any):
        self.input = input
        self.expected = expected
        self.kwargs = kwargs

class PartZero(ABC):
    parsed: dict[Input, Any] = {}

    @staticmethod
    @abstractmethod
    def process(parsed_input: Any, **kwargs: Any) -> int:
        ...

    @staticmethod
    @abstractmethod
    def parse(input: Input) -> Any:
        ...

    @classmethod
    def get_parsed(cls, input: Input) -> Any:
        if input not in cls.parsed:
            cls.parsed[input] = cls.parse(input)
        return cls.parsed[input]

    @classmethod
    def solve(cls, prompt: Prompt) -> bool:
        solution = cls.process(cls.get_parsed(prompt.input), **prompt.kwargs)
        expected = prompt.expected
        if expected is None:
            logger.warning(f"{cls!r} Found {solution:,d} ({solution}). No expected value provided.")
        elif expected == solution:
            logger.success(f"{cls!r} Found {solution:,d} ({solution}).")
        else:
            logger.log("FAILED", f"{cls!r} Found {solution:,d} != expected {expected:,d}.")
        return expected is not None and solution == expected

class Galaxy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance(self, other: "Galaxy") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.x}, {self.y}>"


class Universe:
    def __init__(self, input: list[str]):
        self.x = len(input)
        self.y = len(input[0].strip())

        self.galaxies = set()
        for i in range(len(input)):
            line = input[i].strip()
            for j in range(len(line)):
                if line[j] == "#":
                    self.galaxies.add(Galaxy(i, j))
        self.galaxy_pairs = list(combinations(self.galaxies, 2))

        self.vertical_expansions = sorted(
            list(
                {i for i in range(self.x) if not any((True for g in self.galaxies if g.x == i))}
            )
        )
        self.horizontal_expansions = sorted(
            list(
                {j for j in range(self.y) if not any((True for g in self.galaxies if g.y == j))}
            )
        )
        self.expansion_size = 0

    def expand(self, size: int) -> None:
        self.expansion_size = size

    def count_vertical_expansions_between(self, g1: Galaxy, g2: Galaxy) -> int:
        min_x = min(g1.x, g2.x)
        max_x = max(g1.x, g2.x)
        if min_x > self.vertical_expansions[-1] or max_x < self.vertical_expansions[0]:
            v_count = 0
        else:
            v_min = next(
                (
                    idx for idx, e in enumerate(self.vertical_expansions)
                    if e > min(g1.x, g2.x)
                )
            )
            v_count = next(
                (
                    idx for idx, e in enumerate(self.vertical_expansions[v_min:])
                    if e > max(g1.x, g2.x)
                ),
                len(self.vertical_expansions) - v_min,
            )
        return v_count

    def count_horizontal_expansions_between(self, g1: Galaxy, g2: Galaxy) -> int:
        min_y = min(g1.y, g2.y)
        max_y = max(g1.y, g2.y)
        if min_y > self.horizontal_expansions[-1] or max_y < self.horizontal_expansions[0]:
            h_count = 0
        else:
            h_min = next(
                (
                    idx for idx, e in enumerate(self.horizontal_expansions)
                    if e > min(g1.y, g2.y)
                )
            )
            h_count = next(
                (
                    idx for idx, e in enumerate(self.horizontal_expansions[h_min:])
                    if e > max(g1.y, g2.y)
                ),
                len(self.horizontal_expansions) - h_min,
            )
        return h_count

    def distance(self, galaxies: tuple[Galaxy, Galaxy], expansion_size: int) -> int:
        g1, g2 = galaxies

        v_count = self.count_vertical_expansions_between(g1, g2)
        h_count = self.count_horizontal_expansions_between(g1, g2)

        return g1.distance(g2) + (v_count + h_count) * expansion_size


class PartOne(PartZero):
    @staticmethod
    def parse(input: Input) -> Universe:
        return Universe(input.as_str)

    @staticmethod
    def process(parsed_input: Universe, expansion_size: int) -> int:
        universe = parsed_input
        n = len(universe.galaxies)
        distance_partial = partial(universe.distance, expansion_size=expansion_size)

        return sum(map(distance_partial, universe.galaxy_pairs))

class PartTwo(PartOne):
    pass


test_input = Input("./test_input")
real_input = Input("./input")

def main() -> Iterable[bool]:
    yield PartOne.solve(Prompt(test_input, expected=374, expansion_size=1))
    yield PartOne.solve(Prompt(real_input, expected=9_681_886, expansion_size=1))
    yield PartTwo.solve(Prompt(test_input, expected=1_030, expansion_size=10-1))
    yield PartTwo.solve(Prompt(test_input, expected=8_410, expansion_size=100-1))

if __name__ == "__main__":
    all(main())

def test_results() -> None:
    assert all(main())
