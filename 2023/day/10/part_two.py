import sys

from typing import Optional

from functional import seq
from loguru import logger

from part_one import *

TEST_INPUT_RESULT = 1
REAL_INPUT_RESULT = 269


class PartTwo(PartOne):
    def parse(self) -> "MapPartTwo":
        return MapPartTwo(self.as_str)
    def process(self) -> int:
        map = self.parse()
        r = map.process()
        map.print_matrix(raw=False)
        return r

class PartTwoExample(PartOneExample, PartTwo):
    pass
class PartTwoExampleBis(PartOneExample, PartTwo):
    default_input = "./test_input_2"
class PartTwoExampleTer(PartOneExample, PartTwo):
    default_input = "./test_input_3"
class PartTwoExampleQuad(PartOneExample, PartTwo):
    default_input = "./test_input_4"

class CellPartTwo(Cell):
    def __init__(
        self,
        x: Optional[int]=None,
        y: Optional[int]=None,
        p: Optional[Position]=None,
        c: Optional[str]=None,
        pipe: Optional[Pipe]=None,
        distance: Optional[int]=None,
    ):
        super().__init__(x=x, y=y, p=p, c=c, pipe=pipe, distance=distance)
        self.is_inside = None

    def set_distance(self, distance: int) -> "CellPartTwo":
        self.distance = distance
        self.is_inside = False
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.p}: {self.pipe} (d={self.distance}, inside={'?' if self.is_inside is None else 'T' if self.is_inside else 'F'})>"

class MapPartTwo(Map):
    def process(self) -> int:
        count = 0
        for i in range(self.x):
            for j in range(self.y):
                cell = self[(i, j)]
                if cell.is_inside is not None or cell.distance is not None:
                    continue
                contiguous = self.find_contiguous_cells(cell)
                is_inside = self.is_inside_loop(cell)
                for cell in contiguous:
                    cell.is_inside = is_inside
                if is_inside:
                    count += len(contiguous)
        return count

    @staticmethod
    def make_cell(
        x: Optional[int]=None,
        y: Optional[int]=None,
        p: Optional[Position]=None,
        c: Optional[str]=None,
        pipe: Optional[Pipe]=None,
        distance: Optional[int]=None,
    ) -> CellPartTwo:
        return CellPartTwo(x=x, y=y, p=p, c=c, pipe=pipe, distance=distance)

    def find_contiguous_cells(self, seed: Cell) -> list[Cell]:
        neighbors = []
        candidates = [seed]
        while candidates:
            new_candidates = []
            for candidate in candidates:
                if (
                    candidate.distance is not None
                    or candidate.p.x >= self.x
                    or candidate.p.y >= self.y
                    or candidate in neighbors
                ):
                    continue
                neighbors.append(candidate)
                new_candidates.extend(candidate.all_neighbors(x_max = self.x, y_max=self.y))
            candidates = list(map(self.__getitem__, new_candidates))
        return neighbors

    def reduce_boundary(self, first: list[bool], second: list[bool]) -> list[bool]:
        return [a ^ b for a, b in zip(first, second)]

    def is_inside_loop(self, cell: Cell) -> bool:
        lrud = [
            self.get_boundaries_in_direction(cell, "left"),
            self.get_boundaries_in_direction(cell, "right"),
            self.get_boundaries_in_direction(cell, "up"),
            self.get_boundaries_in_direction(cell, "down"),
        ]

        if any((c for e in lrud if (c := (len(e) == 0)))):
            return False

        r = [seq(l).map(lambda c: c.pipe.lrud).reduce(self.reduce_boundary) for l in lrud]

        left_xor, right_xor, up_xor, down_xor = r
        return (
            left_xor[2] and left_xor[3]
            and right_xor[2] and right_xor[3]
            and up_xor[0] and up_xor[1]
            and down_xor[0] and down_xor[1]
        )

    def get_boundaries_in_direction(self, seed: Cell, direction: str) -> list[Cell]:
        x = seed.p.x
        y = seed.p.y
        match direction:
            case "left":
                boundaries = [
                    cell for j in range(y - 1, -1, -1)
                    if (cell := self[Position(x, j)]).distance is not None
                ]
            case "right":
                boundaries = [
                    cell for j in range(y + 1, self.y)
                    if (cell := self[Position(x, j)]).distance is not None
                ]
            case "up":
                boundaries = [
                    cell for i in range(x - 1, -1, -1)
                    if (cell := self[Position(i, y)]).distance is not None
                ]
            case "down":
                boundaries = [
                    cell for i in range(x + 1, self.x)
                    if (cell := self[Position(i, y)]).distance is not None
                ]
        return boundaries

    def print_matrix(self, raw: bool = True):
        print(f"==={'RAW' if raw else 'PRETTY'}===")
        for i in range(self.x):
            for j in range(self.y):
                cell = self[Position(i, j)]
                if cell.is_start:
                    print("S", end="")
                elif raw:
                    print(cell.raw, end="")
                elif cell.is_inside:
                    print("I", end="")
                else:
                    print(cell.pretty, end="")
            print("")



if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartTwoExample().solve(TEST_INPUT_RESULT)
    PartTwoExampleBis().solve(4)
    PartTwoExampleTer().solve(8)
    PartTwoExampleQuad().solve(10)
    PartTwo(input).solve(REAL_INPUT_RESULT)

def test_test_input__part_two():
    assert PartTwoExample().solve(TEST_INPUT_RESULT)

def test_real_input__part_two():
    assert PartTwo().solve(REAL_INPUT_RESULT)
