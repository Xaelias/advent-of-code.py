import os
from collections.abc import Iterable
from functools import partial
from itertools import combinations
from typing import Any

from functional import seq
from functional.pipeline import Sequence

from aocl.base import AoCInput
from aocl.base import Base


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
            list({i for i in range(self.x) if not any((True for g in self.galaxies if g.x == i))})
        )
        self.horizontal_expansions = sorted(
            list({j for j in range(self.y) if not any((True for g in self.galaxies if g.y == j))})
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
                (idx for idx, e in enumerate(self.vertical_expansions) if e > min(g1.x, g2.x))
            )
            v_count = next(
                (
                    idx
                    for idx, e in enumerate(self.vertical_expansions[v_min:])
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
                (idx for idx, e in enumerate(self.horizontal_expansions) if e > min(g1.y, g2.y))
            )
            h_count = next(
                (
                    idx
                    for idx, e in enumerate(self.horizontal_expansions[h_min:])
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


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return Universe(input_data.as_list_of_str)

    @classmethod
    def process_part_one(
        cls, parsed_input: Universe, expansion_size: int = 1, **kwargs: Any
    ) -> int:  # noqa
        universe = parsed_input
        distance_partial = partial(universe.distance, expansion_size=expansion_size)
        return sum(map(distance_partial, universe.galaxy_pairs))

    @classmethod
    def process_part_two(
        cls, parsed_input: Universe, expansion_size: int = (1000000 - 1), **kwargs: Any
    ) -> int:
        return cls.process_part_one(parsed_input, expansion_size=expansion_size)
