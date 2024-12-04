import math
from typing import Any
from typing import Optional

from functional import seq

from aocl.base import AoCInput
from aocl.base import Base


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


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        directions = input_data.as_list_of_str[0]
        maps = seq(input_data.as_seq[2:]).map(Map.convert).map(lambda m: (m.name, m)).dict()
        return directions, maps

    @classmethod
    def process_part_one(
        cls, parsed_input: Any, start: Optional[str] = "AAA", end="Z", **kwargs: Any
    ) -> int:
        directions, maps = parsed_input

        i = -1
        current = maps[start]
        while not current.name.endswith(end):
            i += 1
            direction = directions[i % len(directions)]
            current = maps[current.next(direction)]
        return i + 1

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        _, maps = parsed_input
        _process = cls.process_part_one
        cycles = seq((m for m in maps if m.endswith("A"))).map(
            lambda start: _process(parsed_input=parsed_input, start=start, end="Z")
        )
        return math.lcm(*cycles)
