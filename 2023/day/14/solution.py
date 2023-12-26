import hashlib
from dataclasses import dataclass
from typing import Any
from typing import Self

import numpy as np

from aocl.base import AoCInput
from aocl.base import Base


class Dish:
    def __init__(self, array: Any) -> None:
        self.array = array

    @property
    def hash(self) -> int:
        return int(hashlib.sha256(self.array.data).hexdigest(), 16)

    def copy(self) -> Self:
        return self.__class__(np.copy(self.array))

    def rotate_left(self) -> None:
        self.array = np.transpose(self.array[::-1])

    def move_north(self) -> None:
        array = self.array
        for j in range(array.shape[1]):
            idx = 0
            repl = []
            for i in range(array.shape[0]):
                if array[i][j] == "O":
                    repl.append("O")
                if array[i][j] == "#" or i == array.shape[0] - 1:
                    if repl:
                        for a in range(len(repl)):
                            array[idx + a][j] = "O"
                        for a in range(idx + len(repl), i + (1 if array[i][j] == "O" else 0)):
                            array[a][j] = "."
                    repl = []
                    idx = i + 1

    def spin_cycle(self) -> None:
        # north
        self.move_north()

        # west
        self.rotate_left()
        self.move_north()

        # south
        self.rotate_left()
        self.move_north()

        # east
        self.rotate_left()
        self.move_north()

        # back to straight up
        self.rotate_left()

    def points(self) -> int:
        return sum([(idx + 1) * np.sum(row) for idx, row in enumerate(self.array[::-1] == "O")])


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return Dish(np.array([list(line) for line in input_data.as_list_of_str]))

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        dish: Dish = parsed_input
        dish.move_north()
        return dish.points()

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        @dataclass
        class Cache:
            result: Any
            spin_cycle: int

        max_spin_cycles_count = int(1e9)

        dish: Dish = parsed_input
        cache: dict[int, Cache] = {}

        spin_cycles_count = 0
        while (h := dish.hash) not in cache:
            dish.spin_cycle()
            cache[h] = Cache(spin_cycle=spin_cycles_count, result=dish.copy())
            spin_cycles_count += 1

        cycle_length = spin_cycles_count - cache[h].spin_cycle
        spin_cycles_count += (
            (max_spin_cycles_count - spin_cycles_count - 1) // cycle_length
        ) * cycle_length

        while (spin_cycles_count := spin_cycles_count + 1) <= max_spin_cycles_count:
            dish = cache[dish.hash].result

        return dish.points()
