from collections import defaultdict
from operator import itemgetter
from typing import Any

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base

Plant = str
Area = int
Edge = tuple[p2.P2, p2.P2]  # defining an edge as the 2 coordinates on each sides, i.e. A|B


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[tuple[Plant, Area, list[Edge]]]:
        farm = input_data.as_strmatrix

        shape = p2.shape(farm)
        rows, cols = shape

        processed = set()

        result = []

        for i in range(rows):
            for j in range(cols):
                if (i, j) in processed:
                    continue

                area = 0  # keep track of number of plants in region on the go
                sides = []  # keep track of sides for perimeter purposes

                to_process = {(i, j)}
                plant = p2.matrix_get(farm, (i, j))
                while to_process:
                    pos = to_process.pop()
                    if pos in processed:
                        continue

                    area += 1  # we found a new plant in the region

                    for neighbor in p2.neighbors(pos):
                        if not p2.in_shape(neighbor, shape):
                            sides.append((pos, neighbor))
                            continue
                        elif p2.matrix_get(farm, neighbor) == plant:
                            to_process.add(neighbor)
                        else:
                            sides.append((pos, neighbor))

                    processed.add(pos)

                result.append((plant, area, sides))
        return result

    @classmethod
    def process_part_one(
        cls, parsed_input: list[tuple[Plant, Area, list[Edge]]], **kwargs: Any
    ) -> int:
        return sum([area * len(sides) for _, area, sides in parsed_input])

    @classmethod
    def count_sides(cls, edges: list[Edge]) -> int:
        grouped_edges = defaultdict(list)

        # group size by direction (from the inside out)
        for side in edges:
            if side[0][0] == side[1][0]:
                if side[0][1] < side[1][1]:
                    grouped_edges[p2.right].append(side[0])
                else:
                    grouped_edges[p2.left].append(side[1])
            else:
                if side[0][0] < side[1][0]:
                    grouped_edges[p2.down].append(side[0])
                else:
                    grouped_edges[p2.up].append(side[1])

        side_count = 4  # at least 4 sides
        # count every "gap" in the list (i.e. a new side)
        for direction in grouped_edges:
            queue = grouped_edges[direction]
            if direction in (p2.left, p2.right):
                move = p2.up
                queue = sorted(queue, key=itemgetter(1, 0))
            else:
                move = p2.left
                queue = sorted(queue, key=itemgetter(0, 1))

            curr = queue.pop()
            while queue:
                next = queue.pop()
                if move(curr) != next:
                    side_count += 1
                curr = next

        return side_count

    @classmethod
    def process_part_two(
        cls, parsed_input: list[tuple[Plant, Area, list[Edge]]], **kwargs: Any
    ) -> int:
        return sum([area * cls.count_sides(sides) for _, area, sides in parsed_input])
