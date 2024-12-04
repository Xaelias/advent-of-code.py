from collections import defaultdict
from typing import Any
from typing import Optional
from typing import Self

from functional import seq

from aocl.base import AoCInput
from aocl.base import Base


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
    LRUD = defaultdict(
        lambda: [F, F, F, F],
        {
            "-": [T, T, F, F],
            "|": [F, F, T, T],
            "J": [T, F, T, F],
            "7": [T, F, F, T],
            "F": [F, T, F, T],
            "L": [F, T, T, F],
        },
    )

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
        x: Optional[int] = None,
        y: Optional[int] = None,
        p: Optional[Position] = None,
        c: Optional[str] = None,
        pipe: Optional[Pipe] = None,
        distance: Optional[int] = None,
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

    def all_neighbors(
        self, x_max: Optional[int] = None, y_max: Optional[int] = None
    ) -> list[Position]:
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
    def __init__(self, input_data: list[str]):
        self.x = len(input_data)
        self.y = len(input_data[0].strip())
        self.cells: list[list[Cell]] = []
        for i in range(len(input_data)):
            self.cells.append([])
            line = input_data[i].strip()
            for j in range(len(line)):
                self.cells[i].append(self.__class__.make_cell(x=i, y=j, c=line[j]))
            if "S" in line:
                self.start = self.cells[i][line.index("S")]
        self.max_distance = self.compute_distances()

    @staticmethod
    def make_cell(
        x: Optional[int] = None,
        y: Optional[int] = None,
        p: Optional[Position] = None,
        c: Optional[str] = None,
        pipe: Optional[Pipe] = None,
        distance: Optional[int] = None,
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
                cell
                for neighbor in new_neighbors
                if (
                    neighbor.x <= self.x
                    and neighbor.y <= self.y
                    and (cell := self[neighbor]).distance is None
                )
            ]
        return distance

    def find_start_neighbors(self) -> list[Cell]:
        neighbors = [
            self[neighbor]
            for neighbor in self.start.all_neighbors()
            if self.start.p in self[neighbor].pipe_neighbors()
        ]
        x = self.start.p.x
        y = self.start.p.y
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


class CellPartTwo(Cell):
    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        p: Optional[Position] = None,
        c: Optional[str] = None,
        pipe: Optional[Pipe] = None,
        distance: Optional[int] = None,
    ):
        super().__init__(x=x, y=y, p=p, c=c, pipe=pipe, distance=distance)
        self.is_inside: Optional[bool] = None

    def set_distance(self, distance: int) -> Self:
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
                if cell.is_inside is not None or cell.distance is not None:  # type: ignore
                    continue
                contiguous = self.find_contiguous_cells(cell)
                is_inside = self.is_inside_loop(cell)
                for cell in contiguous:
                    cell.is_inside = is_inside  # type: ignore
                if is_inside:
                    count += len(contiguous)
        return count

    @staticmethod
    def make_cell(
        x: Optional[int] = None,
        y: Optional[int] = None,
        p: Optional[Position] = None,
        c: Optional[str] = None,
        pipe: Optional[Pipe] = None,
        distance: Optional[int] = None,
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
                new_candidates.extend(candidate.all_neighbors(x_max=self.x, y_max=self.y))
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

        r = [
            seq(boundaries).map(lambda c: c.pipe.lrud).reduce(self.reduce_boundary)
            for boundaries in lrud
        ]

        left_xor, right_xor, up_xor, down_xor = r
        return (
            left_xor[2]
            and left_xor[3]
            and right_xor[2]
            and right_xor[3]
            and up_xor[0]
            and up_xor[1]
            and down_xor[0]
            and down_xor[1]
        )

    def get_boundaries_in_direction(self, seed: Cell, direction: str) -> list[Cell]:
        x = seed.p.x
        y = seed.p.y
        match direction:
            case "left":
                boundaries = [
                    cell
                    for j in range(y - 1, -1, -1)
                    if (cell := self[Position(x, j)]).distance is not None
                ]
            case "right":
                boundaries = [
                    cell
                    for j in range(y + 1, self.y)
                    if (cell := self[Position(x, j)]).distance is not None
                ]
            case "up":
                boundaries = [
                    cell
                    for i in range(x - 1, -1, -1)
                    if (cell := self[Position(i, y)]).distance is not None
                ]
            case "down":
                boundaries = [
                    cell
                    for i in range(x + 1, self.x)
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
                elif cell.is_inside:  # type: ignore
                    print("I", end="")
                else:
                    print(cell.pretty, end="")
            print("")


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Map:
        return Map(input_data.as_list_of_str)

    @classmethod
    def process_part_one(cls, parsed_input: Map, **kwargs: Any) -> int:
        return parsed_input.max_distance

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> MapPartTwo:
        return MapPartTwo(input_data.as_list_of_str)

    @classmethod
    def process_part_two(cls, parsed_input: MapPartTwo, **kwargs: Any) -> int:
        return parsed_input.process()
