from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        pairs = []
        for row in input_data.as_list_of_str:
            pair_1, pair_2 = row.split(",")
            x1, x2 = map(int, pair_1.split("-"))
            y1, y2 = map(int, pair_2.split("-"))
            pairs.append((x1, x2, y1, y2))
        return pairs

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        count = 0
        for x1, x2, y1, y2 in parsed_input:
            count += y1 <= x1 <= x2 <= y2 or x1 <= y1 <= y2 <= x2
        return count

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        count = 0
        for x1, x2, y1, y2 in parsed_input:
            count += x1 <= y2 and y1 <= x2
        return count
