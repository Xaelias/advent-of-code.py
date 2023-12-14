import hashlib
from collections.abc import Iterator
from contextlib import suppress
from typing import Any
from typing import Self

import numpy as np
from loguru import logger
from part_zero import Input
from part_zero import PartZero
from part_zero import Prompt

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")


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


class PartOne(PartZero):
    @classmethod
    def parse(cls, input: Input) -> Dish:
        return Dish(np.array([list(line) for line in input.as_list_of_str]))

    @classmethod
    def process(cls, dish: Dish) -> int:  # type: ignore
        dish.move_north()
        return dish.points()


test_input = Input("./test_input")
real_input = Input("./input")


def main() -> Iterator[bool]:
    yield PartOne.solve(Prompt(test_input, expected=136))
    yield PartOne.solve(Prompt(real_input, expected=110779))


if __name__ == "__main__":
    all(main())
