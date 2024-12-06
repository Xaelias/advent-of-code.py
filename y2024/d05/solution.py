from collections import defaultdict
from collections.abc import Sequence
from typing import Any

from functional import seq

from aocl.base import AoCInput
from aocl.base import Base

# old way of sorting, keeping as a record of how to use `cmp_to_key`
# from functools import cmp_to_key
# from functools import partial
# def cmp(first: int, second: int, rules: dict[int, list[int]]) -> int:
#     if second in rules[first]:
#         return -1
#     if first in rules[second]:
#         return 1
#     return 0
#     # rules_cmp = partial(cmp, rules=rules)
#     # sorted([], key=cmp_to_key(rules_cmp))


def pop_middle(update: Sequence[int]) -> int:
    return update[len(update) // 2]


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> tuple[dict[int, list[int]], list[list[int]]]:
        rules_raw, updates_raw = input_data.as_chunks

        rules = defaultdict(list)
        for first, second in [rule.split("|") for rule in rules_raw]:
            rules[int(first)].append(int(second))

        return rules, [list(map(int, update.split(","))) for update in updates_raw]

    @classmethod
    def process_part_one(
        cls,
        parsed_input: tuple[dict[int, list[list[int]]], list[int]],
        **kwargs: Any,
    ) -> int:
        rules, updates = parsed_input
        return (
            seq(updates)
            .filter_not(
                lambda update: seq(update)
                .zip(update[1:])
                # this is effectively checking whether the list is sorted or not
                # see part_two for a way to do this with actual sort
                .starmap(lambda first, second: first in rules[second])
                .any()
            )
            .map(pop_middle)
            .sum()
        )

    @classmethod
    def process_part_two(
        cls,
        parsed_input: tuple[dict[int, list[int]], list[int]],
        **kwargs: Any,
    ) -> int:
        rules, updates = parsed_input

        class Page(int):
            # `sorted` only uses __lt__, which means that's the only operator we need to override
            # return True if self < other
            def __lt__(self, other) -> bool:
                return other in rules[self]

        return (
            seq(updates)
            # deep conversion to Page so that I can sort
            .map(lambda update: map(Page, update))
            .map(sorted)
            # convert to tuples because `.difference` uses sets under the hood
            # and lists are not hashable
            .map(tuple)
            # only keep updates that are different once sorted, i.e. the ones we fixed
            .difference(seq(updates).map(tuple))
            .map(pop_middle)
            .sum()
        )
