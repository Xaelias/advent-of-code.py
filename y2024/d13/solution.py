from typing import Any

import regex

from aocl import linalg
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
        for a1, a2, b1, b2, c1, c2 in parsed_input:
            # coeffs = [
            #     [a1, b1],
            #     [a2, b2],
            # ]
            # result = [c1, c2]

            # solved = np.linalg.solve(coeffs, result)
            # a, b = [round(e) for e in solved]

            a, b = map(int, linalg.fast_dual_system(a1, b1, c1, a2, b2, c2))

            # if a >= 0 and b >= 0 and np.array_equal(np.dot(coeffs, [a, b]), result):
            if a >= 0 and b >= 0 and a * a1 + b * b1 == c1 and a * a2 + b * b2 == c2:
                moves += 3 * a + b

        return moves
