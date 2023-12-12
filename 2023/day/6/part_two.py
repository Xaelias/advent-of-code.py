import os
import re
import sys

from loguru import logger

from part_one import *


def parse_input(iterable) -> tuple[list[str], list[str]]:
    times = next(iterable).replace(" ", "")
    distances = next(iterable).replace(" ", "")
    times = map(int, re.findall(r"\d+", times))
    distances = map(int, re.findall(r"\d+", distances))

    return list(times), list(distances)

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

    assert process_input(times, distances, brute_force) == 71503
    assert process_input(times, distances, binary_search) == 71503
    assert process_input(times, distances, quadratic) == 71503

def test_input():
    with open(os.path.join(os.path.dirname(__file__), "./input"), "r") as f:
        times, distances = parse_input(iter(f.readlines()))

    assert process_input(times, distances, brute_force) == 36992486
    assert process_input(times, distances, binary_search) == 36992486
    assert process_input(times, distances, quadratic) == 36992486
