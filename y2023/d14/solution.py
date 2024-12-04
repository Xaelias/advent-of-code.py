from typing import Any

from aocl.base import AoCInput
from aocl.base import Base
from aocl.p2 import rotate_matrix_left


def move_north(matrix: tuple[str, ...]) -> tuple[str, ...]:
    new_columns = []
    for column in matrix:
        new_sections = []
        for section in column.split("#"):
            n = section.count("O")
            new_sections.append("O" * n + "." * (len(section) - n))
        new_columns.append("#".join(new_sections))
    return tuple(new_columns)


def spin_cycle(columns: tuple[str, ...]) -> tuple[str, ...]:
    for _ in range(4):
        columns = move_north(columns)
        # rotate left because we are dealing with columns not rows
        columns = rotate_matrix_left(columns)
    return columns


def points(columns: tuple[str, ...]) -> int:
    total = 0
    height = len(columns[0])
    for column in columns:
        for value in range(height, 0, -1):
            if column[height - value] == "O":
                total += value
    return total


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return tuple(input_data.as_columns)

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        columns = parsed_input
        columns = move_north(columns)
        return points(columns)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        columns = parsed_input

        cache: dict[tuple[str, ...], int] = {}

        max_cycle_count = int(1.0e9)
        cycle_count = 0
        while columns not in cache:
            cache[columns] = cycle_count
            columns = spin_cycle(columns)
            cycle_count += 1

        cycle_length = cycle_count - cache[columns]
        cycle_count += ((max_cycle_count - cycle_count - 1) // cycle_length) * cycle_length

        while cycle_count < max_cycle_count:
            columns = spin_cycle(columns)
            cycle_count += 1

        return points(columns)
