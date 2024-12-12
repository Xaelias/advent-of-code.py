from functools import cache
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


@cache
def apply_rules_once(stone: int) -> tuple[int, ...]:
    if stone == 0:
        return (1,)
    stone_s = str(stone)
    stone_l = len(stone_s)
    if stone_l % 2 == 0:
        return (int(stone_s[: stone_l // 2]), int(stone_s[stone_l // 2 :]))
    return (2024 * stone,)


@cache
def count_stones(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    return sum(count_stones(stone, blinks - 1) for stone in apply_rules_once(stone))


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[int]:
        return input_data.as_ints

    @classmethod
    def process_part_one(cls, parsed_input: list[int], **kwargs: Any) -> int:
        return sum([count_stones(stone, 25) for stone in parsed_input])

    @classmethod
    def process_part_two(cls, parsed_input: list[int], **kwargs: Any) -> int:
        return sum([count_stones(stone, 75) for stone in parsed_input])
