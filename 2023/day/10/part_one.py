import os
import pytest
import sys

from typing import Any
from typing import Callable
from typing import Optional

from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from contextlib import suppress
from functional import seq
from functional.pipeline import Sequence
from loguru import logger

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")

TEST_INPUT_RESULT = 8
REAL_INPUT_RESULT = 6815


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
    def parse(self) -> "Map":
        return Map(self.as_str)
    def process(self) -> int:
        map = self.parse()
        map.print_matrix(raw=True)
        map.print_matrix(raw=False)
        return map.max_distance

class PartOneExample(PartOne):
    default_input = "./test_input"

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    def __repr__(self) -> str:
        return f"<Pos: {self.x}, {self.y}>"
    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False
    def __hash__(self) -> int:
        return hash((self.x, self.y))

T = True
F = False
class Pipe:
    char_to_ascii = {
        "-": "═",
        "|": "║",
        "J": "╝",
        "7": "╗",
        "F": "╔",
        "L": "╚",
    }
    LRUD = defaultdict(lambda: [F, F, F, F], {
        "-": [T, T, F, F],
        "|": [F, F, T, T],
        "J": [T, F, T, F],
        "7": [T, F, F, T],
        "F": [F, T, F, T],
        "L": [F, T, T, F],
    })
    def __init__(self, char: str):
        self.char = char
        self.ascii = Pipe.char_to_ascii.get(char)
        self.is_start = self.char == "S"
        self.lrud = self.LRUD[self.char]
    def __str__(self) -> str:
        return self.ascii or self.char
    @property
    def left(self) -> bool:
        return self.lrud[0]
    @property
    def right(self) -> bool:
        return self.lrud[1]
    @property
    def up(self) -> bool:
        return self.lrud[2]
    @property
    def down(self) -> bool:
        return self.lrud[3]

class Cell:
    def __init__(
        self,
        x: Optional[int]=None,
        y: Optional[int]=None,
        p: Optional[Position]=None,
        c: Optional[str]=None,
        pipe: Optional[Pipe]=None,
        distance: Optional[int]=None,
    ):
        if x is not None and y is not None:
            self.p = Position(x, y)
        if p is not None:
            self.p = p
        if c is not None:
            self.pipe = Pipe(c)
        if pipe is not None:
            self.pipe = pipe
        assert self.p
        assert self.pipe

        self.distance = distance

    def __repr__(self) -> str:
        return f"Cell<{self.p}: {self.pipe} (d={self.distance})>"

    @property
    def raw(self) -> str:
        return self.pipe.char

    @property
    def pretty(self) -> str:
        if self.distance is not None:
            return str(self.pipe)
        return self.raw

    @property
    def is_start(self) -> bool:
        return self.pipe.is_start

    def set_distance(self, distance: int) -> "Cell":
        self.distance = distance
        return self

    def all_neighbors(self, x_max: Optional[int]=None, y_max: Optional[int]=None) -> list[Position]:
        x = self.p.x
        y = self.p.y
        all_possible = [
            Position(x - 1, y),
            Position(x + 1, y),
            Position(x, y + 1),
            Position(x, y - 1),
        ]
        possible = [p for p in all_possible if p.x >= 0 and p.y >= 0]
        if x_max:
            possible = [p for p in possible if p.x < x_max]
        if y_max:
            possible = [p for p in possible if p.y < y_max]
        return possible

    def pipe_neighbors(self) -> list[Position]:
        x = self.p.x
        y = self.p.y

        neighbors = set()
        if self.pipe.left:
            neighbors.add(Position(x, y - 1))
        if self.pipe.right:
            neighbors.add(Position(x, y + 1))
        if self.pipe.up:
            neighbors.add(Position(x - 1, y))
        if self.pipe.down:
            neighbors.add(Position(x + 1, y))
        return seq(neighbors).filter(lambda p: p.x >= 0 and p.y >= 0).to_list()


class Map:
    def __init__(self, input: list[str]):
        self.x = len(input)
        self.y = len(input[0].strip())
        self.cells: list[list[Cell]] = []
        for i in range(len(input)):
            self.cells.append([])
            line = input[i].strip()
            for j in range(len(line)):
                self.cells[i].append(self.__class__.make_cell(x=i, y=j, c=line[j]))
            if "S" in line:
                self.start = self.cells[i][line.index("S")]
        self.max_distance = self.compute_distances()

    @staticmethod
    def make_cell(
        x: Optional[int]=None,
        y: Optional[int]=None,
        p: Optional[Position]=None,
        c: Optional[str]=None,
        pipe: Optional[Pipe]=None,
        distance: Optional[int]=None,
    ) -> Cell:
        return Cell(x=x, y=y, p=p, c=c, pipe=pipe, distance=distance)

    def __getitem__(self, i: Any) -> Cell:
        if isinstance(i, Cell):
            i = i.p
        if isinstance(i, Position):
            return self.cells[i.x][i.y]
        if isinstance(i, tuple):
            return self.cells[i[0]][i[1]]
        assert False

    def compute_distances(self) -> int:
        c = self.start
        distance = 0
        self[c].set_distance(distance)

        neighbors = self.find_start_neighbors()
        while neighbors:
            distance += 1
            new_neighbors = []
            for neighbor in neighbors:
                neighbor.set_distance(distance)
                new_neighbors.extend(neighbor.pipe_neighbors())
            neighbors = [
                cell for neighbor in new_neighbors
                if (neighbor.x <= self.x and neighbor.y <= self.y and (cell := self[neighbor]).distance is None)
            ]
        return distance

    def find_start_neighbors(self) -> list[Cell]:
        for neighbor in self.start.all_neighbors():
            pipe_neighbors = self[neighbor].pipe_neighbors()

        neighbors =  [self[neighbor] for neighbor in self.start.all_neighbors() if self.start.p in self[neighbor].pipe_neighbors()]
        x = self.start.p.x
        y = self.start.p.y
        first, second = neighbors
        start_lrud = [
            any((neighbor.p.x == x and (y - neighbor.p.y) == 1 for neighbor in neighbors)),
            any((neighbor.p.x == x and (neighbor.p.y - y) == 1 for neighbor in neighbors)),
            any(((x - neighbor.p.x) == 1 and y == neighbor.p.y for neighbor in neighbors)),
            any(((neighbor.p.x - x) == 1 and y == neighbor.p.y for neighbor in neighbors)),
        ]
        start_char = next((k for k, v in Pipe.LRUD.items() if v == start_lrud))
        self.start.pipe = Pipe(start_char)
        self.start.pipe.is_start = True
        return neighbors

    def print_matrix(self, raw: bool = True) -> None:
        print(f"==={'RAW' if raw else 'PRETTY'}===")
        for i in range(self.x):
            for j in range(self.y):
                cell = self[Position(i, j)]
                if cell.is_start:
                    print("S", end="")
                elif raw:
                    print(cell.raw, end="")
                else:
                    print(cell.pretty, end="")
            print("")



if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartOneExample().solve(TEST_INPUT_RESULT)
    PartOne(input).solve(REAL_INPUT_RESULT)

def test_test_input__part_one():
    assert PartOneExample().solve(TEST_INPUT_RESULT)

def test_real_input__part_one():
    assert PartOne().solve(REAL_INPUT_RESULT)
