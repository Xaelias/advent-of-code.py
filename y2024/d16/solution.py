from heapq import heappop
from heapq import heappush
from typing import Any

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base
from aocl.p2 import RULD

Cost = int
Direction = int
Maze = p2.StrMatrix
Costs = list[list[list[int | None]]]
Path = list[list[list[set[tuple[p2.P2, Direction]]]]]


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> tuple[Maze, Costs, Path]:
        maze = input_data.as_strmatrix
        start = p2.where_in_matrix(maze, "S")[0]

        heap: list[tuple[Cost, p2.P2, Direction]] = [(0, start, 0)]

        size_x, size_y = p2.shape(maze)
        costs: Costs = [[[None for _ in RULD] for _ in range(size_y)] for _ in range(size_x)]
        coming_from: Path = [[[set() for _ in RULD] for _ in range(size_y)] for _ in range(size_x)]

        while heap:
            cost, position, direction = heappop(heap)

            for ddidx in range(4):
                new_cost = cost
                # we can't go back
                if (ddidx + 2) % 4 == direction:
                    continue
                dd = RULD[ddidx]
                xx = position[0] + dd[0]
                yy = position[1] + dd[1]

                # skipping processing coordinates that hit obstacles
                if maze[xx][yy] == "#":
                    continue

                new_cost += 1 if ddidx == direction else 1_001

                saved_cost = costs[xx][yy][ddidx]
                if saved_cost is not None and saved_cost == new_cost:
                    coming_from[xx][yy][ddidx].add((position, direction))
                if saved_cost is None or saved_cost > new_cost:
                    coming_from[xx][yy][ddidx] = {(position, direction)}

                # check that we don't have already a better result for these coordinates / direction combo
                if saved_cost is not None and saved_cost <= new_cost:
                    continue

                # save current result and push coordinates / direction combo for further processing
                costs[xx][yy][ddidx] = new_cost
                heappush(heap, (new_cost, (xx, yy), ddidx))
        return maze, costs, coming_from

    @classmethod
    def process_part_one(cls, parsed_input: tuple[Maze, Costs, Path], **kwargs: Any) -> int:
        maze, costs, _ = parsed_input
        goal = p2.where_in_matrix(maze, "E")[0]
        return min(cost for cost in p2.matrix_get(costs, goal) if cost is not None)

    @classmethod
    def process_part_two(cls, parsed_input: tuple[Maze, Costs, Path], **kwargs: Any) -> int:
        maze, costs, coming_from = parsed_input

        start = p2.where_in_matrix(maze, "S")[0]
        goal = p2.where_in_matrix(maze, "E")[0]
        final_cost = cls.process_part_one(parsed_input)

        benches: set[p2.P2] = {start, goal}

        heap: list[tuple[p2.P2, Direction]] = [(goal, p2.matrix_get(costs, goal).index(final_cost))]
        while heap:
            position, idx = heappop(heap)
            for previous in p2.matrix_get(coming_from, position)[idx]:
                if previous in benches:
                    continue
                benches.add(previous[0])
                heappush(heap, previous)

        return len(benches)
