from typing import Any

import numpy as np
import regex

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[tuple[int, ...]]:
        machines = input_data.raw.split("\n\n")
        return [tuple(map(int, regex.findall(r"(\d+)", machine))) for machine in machines]

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> list[tuple[int, ...]]:
        return [
            (a1, a2, b1, b2, 10000000000000 + x, 10000000000000 + y)
            for a1, a2, b1, b2, x, y in cls.parse(input_data)
        ]

    @classmethod
    def process_part_one(cls, parsed_input: list[tuple[int, ...]], **kwargs: Any) -> int:
        moves = 0
        for a1, a2, b1, b2, x, y in parsed_input:
            coeffs = [
                [a1, b1],
                [a2, b2],
            ]
            result = [x, y]

            solved = np.linalg.solve(coeffs, result)
            a, b = [round(e) for e in solved]

            if a >= 0 and b >= 0 and np.array_equal(np.dot(coeffs, [a, b]), result):
                moves += 3 * a + b

        return moves
