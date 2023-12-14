from collections.abc import Iterable
from contextlib import suppress
from dataclasses import dataclass
from typing import Any

from loguru import logger
from part_one import Dish
from part_one import PartOne
from part_one import real_input
from part_one import test_input
from part_zero import Prompt

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")


@dataclass
class Cache:
    result: Any
    spin_cycle: int


class PartTwo(PartOne):
    @classmethod
    def process(cls, parsed_input: Dish, max_spin_cycles_count: int) -> int:  # type: ignore
        dish = parsed_input
        cache: dict[int, Cache] = {}

        spin_cycles_count = 0
        while (h := dish.hash) not in cache:
            dish.spin_cycle()
            cache[h] = Cache(spin_cycle=spin_cycles_count, result=dish.copy())
            spin_cycles_count += 1

        cycle_length = spin_cycles_count - cache[h].spin_cycle
        spin_cycles_count += (
            (max_spin_cycles_count - spin_cycles_count - 1) // cycle_length
        ) * cycle_length

        while (spin_cycles_count := spin_cycles_count + 1) <= max_spin_cycles_count:
            dish = cache[dish.hash].result

        return dish.points()


def main() -> Iterable[bool]:
    yield PartTwo.solve(Prompt(test_input, expected=64, max_spin_cycles_count=1_000_000_000))
    yield PartTwo.solve(Prompt(real_input, expected=86069, max_spin_cycles_count=1_000_000_000))


if __name__ == "__main__":
    all(main())
