import os
from typing import Any
from typing import Optional

from aocl.base import AoCInput
from aocl.base import Base
from aocl.linalg import quadratic_solve
from aocl.p2 import P2
from aocl.p2 import neighbors


def advance_n_steps(
    matrix: list[list[str]], occupied: set[P2], steps: int, enforce_boundaries: bool = True
) -> set[P2]:
    boundaries = (len(matrix), len(matrix[0]))
    for i in range(steps):
        new_occupied = set()
        for position in occupied:
            for candidate in neighbors(position, boundaries if enforce_boundaries else None):
                xx, yy = candidate
                if matrix[xx % boundaries[0]][yy % boundaries[1]] == "#":
                    continue
                new_occupied.add(candidate)
        occupied = new_occupied
    return occupied


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.as_list_of_lists

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        matrix: list[list[str]] = parsed_input
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == "S":
                    start = (i, j)
                    break
                else:
                    continue
                break  # noqa

        occupied = {start}
        return len(advance_n_steps(parsed_input, occupied, 64))

    @classmethod
    def process_part_two(
        cls, parsed_input: Any, steps: Optional[list[int]] = None, **kwargs: Any
    ) -> int | str:
        matrix: list[list[str]] = parsed_input
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == "S":
                    start = (i, j)
                    break
                else:
                    continue
                break  # noqa

        offset = n // 2
        results: list[int] = []

        occupied = {start}
        prev_threshold = 0
        if steps:
            # just run through the all the steps
            results = []
            for threshold in steps:
                occupied = advance_n_steps(
                    matrix, occupied, threshold - prev_threshold, enforce_boundaries=False
                )
                results.append(len(occupied))
                prev_threshold = threshold
            return ", ".join(map(str, results))

        for threshold in [i * n + offset for i in range(3)]:
            occupied = advance_n_steps(
                matrix, occupied, threshold - prev_threshold, enforce_boundaries=False
            )
            results.append(len(occupied))
            prev_threshold = threshold

        return int(quadratic_solve((26501365 - offset) // n, *enumerate(results)))


def main() -> None:
    _, year, _, day = os.path.dirname(__file__).rsplit("/", maxsplit=3)
    Solution(year=year, day=day).solve_all()


if __name__ == "__main__":
    main()
