import os
from typing import Any

from aocl.algo.dijkstra import dijkstra
from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.as_nparray.astype(int)

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        return dijkstra(
            parsed_input,
            start=(0, 0),
            goal=(parsed_input.shape[0] - 1, parsed_input.shape[1] - 1),
            max_distance=3,
        )

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        return dijkstra(
            parsed_input,
            start=(0, 0),
            goal=(parsed_input.shape[0] - 1, parsed_input.shape[1] - 1),
            min_distance=4,
            max_distance=10,
        )


def main() -> None:
    _, year, _, day = os.path.dirname(__file__).rsplit("/", maxsplit=3)
    Solution(year=year, day=day).solve_all()


if __name__ == "__main__":
    main()
