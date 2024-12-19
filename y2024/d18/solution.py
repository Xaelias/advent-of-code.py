from typing import Any

from aocl import p2
from aocl.algo.dijkstra import dijkstra
from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import logger


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> tuple[p2.P2, ...]:
        bytes = (pair.split(",") for pair in input_data.as_lines)
        """
        Each byte position is given as an X,Y coordinate,
        where X is the distance from the left edge of your memory space
        and Y is the distance from the top edge of your memory space.
        """
        return tuple((int(x), int(y)) for (y, x) in bytes)

    @classmethod
    def process_part_one(cls, parsed_input: tuple[p2.P2, ...], **kwargs: Any) -> int:
        width = int(kwargs.get("width", 71))
        corrupted = parsed_input[: int(kwargs.get("bytes", 1024))]
        memory = [[1_000 if (i, j) in corrupted else 1 for j in range(width)] for i in range(width)]

        return dijkstra(memory, (0, 0), (width - 1, width - 1))

    @classmethod
    def process_part_two(cls, parsed_input: tuple[p2.P2, ...], **kwargs: Any) -> str:
        width = int(kwargs.get("width", 71))
        corrupted = parsed_input

        idx_min = 0
        idx_max = len(corrupted)
        idx = idx_max // 2
        while not (idx_min + 1 == idx_max):
            logger.info(f"Trying with {idx} ({idx_min} / {idx_max}) corrupted bytes.")
            memory = [
                [1_000 if (i, j) in corrupted[:idx] else 1 for j in range(width)]
                for i in range(width)
            ]
            if dijkstra(memory, (0, 0), (width - 1, width - 1)) >= 1_000:
                idx_max = idx
            else:
                idx_min = idx
            idx = (idx_max - idx_min) // 2 + idx_min
        return f"{corrupted[idx][1]},{corrupted[idx][0]}"
