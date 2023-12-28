from collections import defaultdict
from functools import cache
from itertools import combinations
from typing import Any
from typing import Optional

import numpy as np

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base
from aocl.p2 import in_shape
from aocl.p2 import P2


def longest_path(
    carte, current_position: P2, finish: P2, last_position: Optional[P2] = None, cost=0
) -> int:
    if current_position == finish:
        return cost
    next_move: Optional[P2]
    match carte[current_position[0]][current_position[1]]:  # noqa
        case ">":
            next_move = p2.right(current_position)
        case "<":
            next_move = p2.left(current_position)
        case "^":
            next_move = p2.up(current_position)
        case "v":
            next_move = p2.down(current_position)
        case _:
            next_move = None

    if next_move is None:
        next_positions = [
            p2.left(current_position),
            p2.right(current_position),
            p2.up(current_position),
            p2.down(current_position),
        ]
    else:
        next_positions = [next_move]

    possible_cost = -100000000000
    for position in next_positions:
        if not p2.in_shape(position, carte.shape):
            continue
        if position == last_position:
            continue
        if carte[position[0], position[1]] == "#":
            continue
        possible_cost = max(
            possible_cost, longest_path(carte, position, finish, current_position, cost + 1)
        )
    return possible_cost


class Solution(Base):
    @classmethod
    @cache
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.as_nparray

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        carte = parsed_input
        where = np.where(parsed_input[0] == ".")
        start = (0, int(where[0][0]))
        where = np.where(parsed_input[-1] == ".")
        finish = (parsed_input.shape[0] - 1, int(where[0][0]))

        return longest_path(carte, start, finish)

    @classmethod
    @cache
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        carte = cls.parse(input_data)
        where = np.where(carte[0] == ".")
        start = (0, int(where[0][0]))
        where = np.where(carte[-1] == ".")
        finish = (carte.shape[0] - 1, int(where[0][0]))

        intersections = []
        for i in range(carte.shape[0]):
            for j in range(carte.shape[1]):
                if carte[i][j] == "#":
                    continue
                valid_directions = 0
                for ddidx in range(4):
                    dd = p2.RULD[ddidx]
                    xx = i + dd[0]
                    yy = j + dd[1]
                    if not in_shape((xx, yy), carte.shape):
                        continue
                    if carte[xx][yy] == "#":
                        continue
                    valid_directions += 1
                if valid_directions >= 3:
                    intersections.append((i, j))

        # now to find the longest path between any two intersections (without going another intersection)
        blocked_carte = np.copy(carte)
        for intersection in intersections:
            blocked_carte[intersection[0]][intersection[1]] = "#"
        for i in range(blocked_carte.shape[0]):
            for j in range(blocked_carte.shape[1]):
                if str(blocked_carte[i][j]) in "<>^v":
                    blocked_carte[i][j] = "."

        intersection_distances: dict[P2, dict[P2, int]] = defaultdict(dict)
        for i1, i2 in combinations(intersections, 2):
            blocked_carte[i1[0]][i1[1]] = "."
            blocked_carte[i2[0]][i2[1]] = "."

            distance = longest_path(blocked_carte, i1, i2)

            blocked_carte[i1[0]][i1[1]] = "#"
            blocked_carte[i2[0]][i2[1]] = "#"
            if distance > 0:
                intersection_distances[i1][i2] = distance
                intersection_distances[i2][i1] = distance

        for intersection in intersections:
            blocked_carte[intersection[0]][intersection[1]] = "."
            distance = longest_path(blocked_carte, start, intersection)
            blocked_carte[intersection[0]][intersection[1]] = "#"
            if distance > 0:
                intersection_distances[start][intersection] = distance
                break

        for intersection in intersections:
            blocked_carte[intersection[0]][intersection[1]] = "."
            distance = longest_path(blocked_carte, finish, intersection)
            blocked_carte[intersection[0]][intersection[1]] = "#"
            if distance > 0:
                intersection_distances[intersection][finish] = distance
                break
        return intersection_distances, start, finish

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        graph, start, finish = parsed_input

        def crawl_fast(graph, start, finish):
            heap = [(start, 0)]
            seen = set()
            while heap:
                position, distance = heap.pop()
                if distance == -1:
                    seen.remove(position)
                    continue
                seen.add(position)
                heap.append((position, -1))
                for next_pos, cost in graph[position].items():
                    if next_pos == finish:
                        yield distance + cost
                        continue
                    if next_pos in seen:
                        continue
                    heap.append((next_pos, cost + distance))

        total_distance = max(crawl_fast(graph, start, finish))

        return total_distance
