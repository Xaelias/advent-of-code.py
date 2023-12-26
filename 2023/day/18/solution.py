from typing import Any

from aocl.algo.pick import Pick
from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        r = []
        for line in input_data.as_list_of_str:
            direction, distance, color = line.split()
            r.append((direction, int(distance), color[2:-1]))
        return r

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        dir_dist = [(direction, distance) for direction, distance, _ in parsed_input]

        return Pick.area_from_direction_distance_tuples(dir_dist)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        dir_dist = []
        for row in parsed_input:
            _, _, color = row

            # rgb == #70c710, ignore # and ignore last digit for direction
            distance = int(color[:-1], 16)
            # 0 == R, 1 == D, 2 == L, 3 == U
            dd = "RDLU"[int(color[-1])]
            # could also just call back part one with a list of (dd, distance, _)
            dir_dist.append((dd, distance))
        return Pick.area_from_direction_distance_tuples(dir_dist)
