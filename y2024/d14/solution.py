import functools
import operator
from typing import Any

import regex

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import logger


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[tuple[int, ...]]:
        pattern = r"-?\d+"
        return [tuple(map(int, regex.findall(pattern, line))) for line in input_data.as_lines]

    @classmethod
    def process_part_one(cls, parsed_input: list[tuple[int, ...]], **kwargs: Any) -> int:
        width = kwargs.get("width", 101)
        height = kwargs.get("height", 103)

        mid_width = width // 2
        mid_height = height // 2

        quadrants = [0, 0, 0, 0]
        for x, y, vx, vy in parsed_input:
            f1 = (x + 100 * vx) % width
            f2 = (y + 100 * vy) % height

            if not (f1 == mid_width or f2 == mid_height):
                quadrant = f1 // (mid_width + 1) + f2 // (mid_height + 1) * 2
                quadrants[quadrant] += 1

        return functools.reduce(operator.mul, quadrants)

    @classmethod
    def render_map(cls, width: int, height: int, positions: set[p2.P2]) -> str:
        drawing = [
            "".join(["#" if (i, j) in positions else " " for i in range(height)])
            for j in range(width)
        ]
        return "\n".join([""] + drawing)

    @classmethod
    def process_part_two(cls, parsed_input: list[tuple[int, ...]], **kwargs: Any) -> int:
        width = kwargs.get("width", 101)
        height = kwargs.get("height", 103)
        bots = parsed_input

        for count in range(1, 1_000_000):
            positions = set()
            for x, y, vx, vy in bots:
                f1 = (x + count * vx) % width
                f2 = (y + count * vy) % height

                if (f1, f2) in positions:
                    break
                positions.add((f1, f2))
            else:
                logger.info(cls.render_map(width, height, positions))
                break
        return count
