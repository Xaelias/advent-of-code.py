import math
import re
from functools import reduce
from math import ceil
from math import floor
from typing import Any

import sympy
from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base


def brute_force(time: int, distance: int) -> int:
    solutions = [i for i in range(time) if i * (time - i) > distance]
    return solutions[-1] - solutions[0] + 1


def _binary_search(time: int, distance: int, hold: int, delta: int, minimize: bool) -> int:
    logger.trace(f"_binary_search step: {time=}, {distance=}, {hold=}, {delta=}, {minimize=}")
    sign = 1 if minimize else -1

    current_result = hold * (time - hold)
    next_result = (hold - sign) * (time - (hold - sign))

    stop_recursion = current_result > distance >= next_result
    logger.trace(f"{stop_recursion=}, {current_result=}, {next_result=}, {distance=}")
    if stop_recursion:
        return hold

    delta = max(delta // 2, 1)
    if current_result > distance:
        sign = -sign
    return _binary_search(time, distance, hold + sign * delta, delta, minimize)


def binary_search(time: int, distance: int) -> int:
    start = _binary_search(time, distance, 0, time // 2, True)
    end = _binary_search(time, distance, time, time // 2, False)
    return end - start + 1


def quadratic(time: int, distance: int) -> int:
    # ax^2 + bx + c = 0
    #     -b ± sqrt(b**2 - 4ac)
    # x = --------------------
    #              2a
    #
    # d = x * (t - x)
    # x**2 - xt + d = 0
    #
    # we want to solve:
    # x**2 -xt -d > 0
    # i.e. a=1, b=-t, c=d
    #     t ± sqrt(t**2 - 4d)
    # x > -------------------
    #             2
    t = time
    d = distance + 1  # to account for > vs. >=
    start = (t - (t**2 - 4 * d) ** 0.5) / 2
    end = (t + (t**2 - 4 * d) ** 0.5) / 2
    logger.trace(f"Quadratic solve for {time=}, {distance=} gives {start=}, {end=}")
    return int(floor(end) - ceil(start) + 1)


def with_sympy(time: int, distance: int) -> int:
    x = sympy.symbols("x")
    solutions = sympy.solve(x**2 + time * x + distance)
    return int(math.floor(solutions[1]) - math.ceil(solutions[0]) + 1)


def process_input(times: list[int], distances: list[int], algo):
    logger.info(f"Solving problem using algo={algo.__name__}: {times=}, {distances=}")
    result = reduce(lambda x, y: x * y, [algo(t, d) for t, d in zip(times, distances)])
    logger.success(f"Solution using {algo.__name__} is {result:,d} ({result}).")
    return result


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        times = list(map(int, re.findall(r"\d+", input_data.as_list_of_str[0])))
        distances = list(map(int, re.findall(r"\d+", input_data.as_list_of_str[1])))
        return times, distances

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        times, distances = parsed_input
        # return process_input(times, distances, brute_force)  # works
        # return process_input(times, distances, binary_search)  # works
        return process_input(times, distances, quadratic)  # works
        # return process_input(times, distances, with_sympy)  # slow

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        time = int(input_data.as_list_of_str[0].split(":")[1].replace(" ", ""))
        distance = int(input_data.as_list_of_str[1].split(":")[1].replace(" ", ""))
        return time, distance

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        time, distance = parsed_input
        # return brute_force(time, distance)  # very slow
        # return binary_search(time, distance)  # works
        return quadratic(time, distance)  # works
        # return with_sympy(time, distance)  # slow-ish
