import itertools
import operator
from collections import defaultdict
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base

City = str
Distance = int


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> dict[tuple[City, ...], Distance]:
        distances: dict[City, dict[City, Distance]] = defaultdict(dict)
        for line in input_data.as_lines:
            departure, _, arrival, _, distance = line.split()
            distances[departure][arrival] = int(distance)
            distances[arrival][departure] = int(distance)
        cities = sorted(distances)

        results = {}
        for order in itertools.permutations(cities):
            order_distance = 0
            for departure, arrival in zip(order, order[1:]):
                order_distance += distances[departure][arrival]
            results[order] = order_distance

        return results

    @classmethod
    def process_part_one(cls, parsed_input: dict[tuple[City, ...], Distance], **kwargs: Any) -> int:
        return min(parsed_input.items(), key=operator.itemgetter(1))[1]

    @classmethod
    def process_part_two(cls, parsed_input: dict[tuple[City, ...], Distance], **kwargs: Any) -> int:
        return max(parsed_input.items(), key=operator.itemgetter(1))[1]
