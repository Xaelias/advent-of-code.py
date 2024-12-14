from typing import Any

import numpy as np
import regex
from numpy.typing import NDArray

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> tuple[NDArray, NDArray]:
        pattern = r"-?\d+"
        everything = [list(map(int, regex.findall(pattern, line))) for line in input_data.as_lines]

        return np.array([[x, y] for x, y, _, _ in everything]), np.array(
            [[vx, vy] for _, _, vx, vy in everything]
        )

    @classmethod
    def process_part_one(cls, parsed_input: tuple[NDArray, NDArray], **kwargs: Any) -> int:
        width = kwargs.get("width", 101)
        height = kwargs.get("height", 103)

        mid_width = width // 2
        mid_height = height // 2

        positions, movements = parsed_input
        new_positions = (positions + 100 * movements) % (width, height)

        return np.prod(
            np.unique(  # 3. count element in each quadrants
                np.delete(  # 1. remove elements in the middle
                    new_positions,
                    np.where(
                        (new_positions[:, 0] == mid_width) | (new_positions[:, 1] == mid_height)
                    ),
                    axis=0,
                )
                // (mid_width + 1, mid_height + 1),  # 2. assign to quadrants
                return_counts=True,
                axis=0,
            )[1]
        )

    @classmethod
    def process_part_two(cls, parsed_input: tuple[NDArray, NDArray], **kwargs: Any) -> int:
        width = kwargs.get("width", 101)
        height = kwargs.get("height", 103)

        positions, movements = parsed_input
        for i in range(1, 1_000_000):
            new_positions = (positions + i * movements) % (width, height)

            if len(np.unique(new_positions, return_counts=True, axis=0)[1]) == len(positions):
                break
        return i
