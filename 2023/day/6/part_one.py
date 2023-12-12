import os
import pytest
import re
import sys

from functools import reduce
from loguru import logger
from math import ceil, floor
from typing import Optional

def brute_force(time: int, distance: int) -> int:
    solutions = [i for i in range(time) if i * (time - i) > distance]
    return solutions[-1] - solutions[0] + 1


def _binary_search(time: int, distance: int, hold: int, delta: int, minimize: bool) -> int:
    logger.trace(f"_binary_search step: {time=}, {distance=}, {hold=}, {delta=}, {minimize=}")
    sign = 1 if minimize else -1

    current_result = hold * (time - hold)
    next_result = (hold - sign) * (time - (hold - sign))

    stop_recursion = current_result > distance and next_result <= distance
    logger.trace(f"{stop_recursion=}, {current_result=}, {next_result=}, {distance=}")
    if stop_recursion:
        return hold

    delta = max(delta // 2, 1)
    if current_result > distance:
        sign = - sign
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
    start = (t - (t**2 - 4*d)**.5)/2
    end = (t + (t**2 - 4*d)**.5)/2
    logger.trace(f"Quadratic solve for {time=}, {distance=} gives {start=}, {end=}")
    return int(floor(end) - ceil(start) + 1)


def parse_input(iterable) -> tuple[list[str], list[str]]:
    times = next(iterable)
    distances = next(iterable)
    times = map(int, re.findall(r"\d+", times))
    distances = map(int, re.findall(r"\d+", distances))

    return list(times), list(distances)

def process_input(times: list[int], distances: list[int], algo):
    logger.info(f"Solving problem using algo={algo.__name__}: {times=}, {distances=}")
    result = reduce(lambda x, y: x * y, [algo(t, d) for t, d in zip(times, distances)])
    logger.success(f"Solution using {algo.__name__} is {result:,d} ({result}).")
    return result


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./input")
    possible_games = []
    with open(input, "r") as f:
        times, distances = parse_input((line.strip() for line in f.readlines()))
        process_input(times, distances, brute_force)
        process_input(times, distances, binary_search)
        process_input(times, distances, quadratic)


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)


def run_algo_on_test_input(method):
    assert method(7, 9) == 4
    assert method(15, 40) == 8
    assert method(30, 200) == 9

def test_algos():
    run_algo_on_test_input(brute_force)
    run_algo_on_test_input(binary_search)
    run_algo_on_test_input(quadratic)

TEST_INPUT = """
Time:      7  15   30
Distance:  9  40  200
""".split("\n")[1:-1]
def test_test_input():
    times, distances = parse_input(iter(TEST_INPUT))

    assert process_input(times, distances, brute_force) == 288
    assert process_input(times, distances, binary_search) == 288
    assert process_input(times, distances, quadratic) == 288

def test_input():
    with open(os.path.join(os.path.dirname(__file__), "./input"), "r") as f:
        times, distances = parse_input(iter(f.readlines()))

    assert process_input(times, distances, brute_force) == 252000
    assert process_input(times, distances, binary_search) == 252000
    assert process_input(times, distances, quadratic) == 252000
