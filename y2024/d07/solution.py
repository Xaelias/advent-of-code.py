from operator import add
from operator import mul
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


def do_math(numbers: list[int], operators: list = [add, mul]) -> list[int]:
    if len(numbers) == 1:
        return numbers
    head, *tail = numbers
    # we do next_elemtn op head in that order because we're processing the list in reverse
    return [op(next_element, head) for next_element in do_math(tail, operators) for op in operators]


class Solution(Base):
    # save results of part one to speed up part two
    # does not change anything if part one is not ran (just makes part two slower)
    part_one_solutions: list[int] = []

    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[int]]:
        return (
            input_data.as_seq.map(lambda line: line.replace(":", ""))
            .map(str.split)
            .map(lambda line: list(map(int, line)))
            .to_list()
        )

    @classmethod
    def process_part_one(cls, parsed_input: list[list[int]], **kwargs: Any) -> int:
        cls.part_one_solutions = []
        for result, *numbers in parsed_input:
            candidates = do_math(numbers[::-1])
            if result in candidates:
                cls.part_one_solutions.append(result)
        return sum(cls.part_one_solutions)

    @classmethod
    def process_part_two(cls, parsed_input: list[list[int]], **kwargs: Any) -> int:
        total = 0
        for result, *numbers in parsed_input:
            if result in cls.part_one_solutions:
                total += result
                continue
            candidates = do_math(numbers[::-1], operators=[add, mul, concat])
            total += result if result in candidates else 0
        return total
