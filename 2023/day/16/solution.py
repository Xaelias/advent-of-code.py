from contextlib import suppress
from typing import Any

import numpy as np
from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base

with suppress(Exception):
    logger.level("FAILED", no=25, color="<red>")


def propagate_light(contraption, left, right, up, down, position, direction: str):
    a, b = position

    if a < 0 or b < 0 or a >= contraption.shape[0] or b >= contraption.shape[1]:
        return []

    match direction:
        case "left":
            arr = left
        case "right":
            arr = right
        case "up":
            arr = up
        case "down":
            arr = down
        case _:
            raise ValueError(f"Invalid direction {direction!r}")

    if arr[a][b]:
        return []

    arr[a][b] = True
    match contraption[a][b]:
        case ".":
            if direction == "left":
                x = a
                y = b - 1
            elif direction == "right":
                x = a
                y = b + 1
            elif direction == "up":
                x = a - 1
                y = b
            elif direction == "down":
                x = a + 1
                y = b
            else:
                raise ValueError(f"Invalid direction {direction!r}")
            return [(x, y, direction)]
        case "|":
            if direction == "left" or direction == "right":
                return [(a - 1, b, "up"), (a + 1, b, "down")]
            elif direction == "up":
                return [(a - 1, b, direction)]
            else:
                return [(a + 1, b, direction)]
        case "-":
            if direction == "up" or direction == "down":
                return [(a, b - 1, "left"), (a, b + 1, "right")]
            elif direction == "left":
                return [(a, b - 1, direction)]
            else:
                return [(a, b + 1, direction)]
        case "\\":
            if direction == "left":
                x = a - 1
                y = b
                new_direction = "up"
            elif direction == "right":
                x = a + 1
                y = b
                new_direction = "down"
            elif direction == "up":
                x = a
                y = b - 1
                new_direction = "left"
            elif direction == "down":
                x = a
                y = b + 1
                new_direction = "right"
            else:
                raise ValueError(f"Invalid direction {direction!r}")
            return [(x, y, new_direction)]
        case "/":
            if direction == "right":
                x = a - 1
                y = b
                new_direction = "up"
            elif direction == "left":
                x = a + 1
                y = b
                new_direction = "down"
            elif direction == "down":
                x = a
                y = b - 1
                new_direction = "left"
            elif direction == "up":
                x = a
                y = b + 1
                new_direction = "right"
            else:
                raise ValueError(f"Invalid direction {direction!r}")
            return [(x, y, new_direction)]
        case _:
            raise ValueError(f"Don't know what to do with {contraption[a][b]}")


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return np.array([list(line) for line in input_data.as_list_of_str])

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        contraption = parsed_input

        left = np.full(contraption.shape, False)
        right = np.full(contraption.shape, False)
        up = np.full(contraption.shape, False)
        down = np.full(contraption.shape, False)

        heap = [(0, 0, "right")]
        while heap:
            x, y, direction = heap.pop()
            heap.extend(propagate_light(contraption, left, right, up, down, (x, y), direction))

        total = left + right + up + down
        return np.sum(total)  # type: ignore

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        contraption = parsed_input

        entrypoints = (
            [(0, j, "down") for j in range(contraption.shape[1])]
            + [(contraption.shape[0] - 1, j, "up") for j in range(contraption.shape[1])]
            + [(i, 0, "right") for i in range(contraption.shape[0])]
            + [(i, contraption.shape[1] - 1, "left") for i in range(contraption.shape[0])]
        )

        results = []
        for entrypoint in entrypoints:
            heap = [entrypoint]
            left = np.full(contraption.shape, False)
            right = np.full(contraption.shape, False)
            up = np.full(contraption.shape, False)
            down = np.full(contraption.shape, False)
            while heap:
                x, y, direction = heap.pop()
                heap.extend(propagate_light(contraption, left, right, up, down, (x, y), direction))
            result = np.sum(left + right + up + down)
            results.append(result)

        return max(results)  # type: ignore
