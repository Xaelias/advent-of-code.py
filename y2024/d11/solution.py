from collections import defaultdict
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


# basically https://www.reddit.com/r/adventofcode/comments/1hbm0al/comment/m1hp3e3/
def iterative_count(stones: list[int], blinks: int) -> int:
    counts = {stone: 1 for stone in stones}
    for _ in range(blinks):
        new_counts: dict[int, int] = defaultdict(int)
        for st in counts:
            for blked in ~(w := len(str(st))) % 2 * divmod(st, 10 ** (w // 2)) or [st * 2024 or 1]:
                new_counts[blked] += counts[st]
        counts = new_counts
    return sum(counts.values())


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[int]:
        return input_data.as_ints

    @classmethod
    def process_part_one(cls, parsed_input: list[int], **kwargs: Any) -> int:
        blinks = 25
        # return sum([count_stones(stone, blinks) for stone in parsed_input])
        return iterative_count(parsed_input, blinks)

    @classmethod
    def process_part_two(cls, parsed_input: list[int], **kwargs: Any) -> int:
        blinks = 75
        # return sum([count_stones(stone, blinks) for stone in parsed_input])
        return iterative_count(parsed_input, blinks)
