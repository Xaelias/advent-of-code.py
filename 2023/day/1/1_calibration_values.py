from loguru import logger

import os
import sys
import re


def find_first_and_last_number(line: str) -> int:
    """Find first and last number in a string"""
    numbers = re.sub(r"\D+", "", line)
    first = numbers[0]
    last = numbers[-1]
    total = int(first + last)
    logger.debug(f"Processed line. [{line=}, {numbers=}, {first=}, {last=}, {total=}]")
    return total


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./0_input")
    with open(input, "r") as f:
        total = sum((find_first_and_last_number(line.strip()) for line in f.readlines()), 0)
    logger.info(f"The total for the dataset is: {total}")
    return total


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)


def test_two_numbers():
    assert find_first_and_last_number("19") == 19


def test_one_number():
    assert find_first_and_last_number("1") == 11


def test_provided():
    assert find_first_and_last_number("1abc2") == 12
    assert find_first_and_last_number("pqr3stu8vwx") == 38
    assert find_first_and_last_number("a1b2c3d4e5f") == 15
    assert find_first_and_last_number("treb7uchet") == 77


def test_real():
    assert main(None) == 56042
