#!/usr/bin/env python3V
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur <Me@ALesieur.net>
# Date              : 2023/12/03 10:45:46
# Last Modified Date: 2023/12/03 11:19:31
# Last Modified By  : Alexis Lesieur <Me@ALesieur.net>
from loguru import logger
from typing import Optional

import os
import re
import sys


digits = [str(d) for d in range(0, 10)]


def find_mult_indexes(line: str) -> list[int]:
    return [i for i in range(len(line or "")) if line[i] == "*"]


def extract_number_at_index(line: str, index: int) -> Optional[int]:
    logger.trace(f"Trying to extract numbers from {line=} at {index=}.")

    if not line:
        logger.trace(f"Skipping empty line. [{line=}]")
        return None, line

    if index < 0:
        logger.trace(f"Skipping index < 0. [{line=}, {index=}]")
        return None, line

    if index >= len(line):
        logger.trace(f"Skipping index >= len(line). [{line=}, {len(line)=}, {index=}]")
        return None, line

    if line[index] in digits:
        logger.trace(f"Found a number! Extracting. [{line=}, {index=}, {line[index]=}]")
        s = ""
        s = line[index]

        i = 1
        while index - i >= 0 and line[index - i] in digits:
            s = line[index - i] + s
            i += 1
        start = index - i + 1
        i = 1
        while index + i < len(line) and line[index + i] in digits:
            s = s + line[index + i]
            i += 1
        end = index + i - 1

        number = int(s)
        new_line = line[0:start] + "."*len(s) + line[end+1:]
        logger.debug(f"Replaced found number with '.'s. [{line=}, {number=}, {new_line=}]")
        return number, new_line
    return None, line



def find_adjacent_numbers(previous_line: Optional[str], current_line: str, next_line: Optional[str], index: int) -> [int]:
    logger.trace(f"Extract from previous line.")
    numbers = []
    number, previous_line = extract_number_at_index(previous_line, index - 1)
    numbers.append(number)
    number, previous_line = extract_number_at_index(previous_line, index)
    numbers.append(number)
    number, previous_line = extract_number_at_index(previous_line, index + 1)
    numbers.append(number)

    number, current_line = extract_number_at_index(current_line, index - 1)
    numbers.append(number)
    number, current_line = extract_number_at_index(current_line, index)
    numbers.append(number)
    number, current_line = extract_number_at_index(current_line, index + 1)
    numbers.append(number)

    number, next_line = extract_number_at_index(next_line, index - 1)
    numbers.append(number)
    number, next_line = extract_number_at_index(next_line, index)
    numbers.append(number)
    number, next_line = extract_number_at_index(next_line, index + 1)
    numbers.append(number)

    return [number for number in numbers if number is not None]

def process_line(line: str, provided_indexes: list[int]) -> list[int]:
    results = []

    my_symbols = find_symbols_indexes(line)
    logger.trace(f"Processing line self indexes. [{line=}, {my_symbols=}]")
    for symbol in my_symbols:
        number, line = extract_number_at_index(line, symbol - 1)
        if number:
            results.append(number)
        number, line = extract_number_at_index(line, symbol + 1)
        if number:
            results.append(number)

    logger.trace(f"Processing line with provided indexes. [{line=}, {provided_indexes=}].")
    for symbol in provided_indexes:
        number, line = extract_number_at_index(line, symbol - 1)
        if number:
            results.append(number)
            number = None
        else:
            number, line = extract_number_at_index(line, symbol)
        if number:
            results.append(number)
            number = None
        else:
            number, line = extract_number_at_index(line, symbol + 1)
        if number:
            results.append(number)
    return results, my_symbols, line


def process_input(iterable) -> int:
    previous_line = None
    current_line = None
    next_line = None
    total = 0
    for line in iterable:
        previous_line = current_line
        current_line = next_line
        next_line = line

        mult_symbols = find_mult_indexes(current_line)
        for index in mult_symbols:
            numbers = find_adjacent_numbers(previous_line, current_line, next_line, index)
            if len(numbers) == 2:
                total += numbers[0] * numbers[1]
    return total


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./input")
    possible_games = []
    with open(input, "r") as f:
        total = process_input((line.strip() for line in f.readlines()))
        logger.info(f"Solution is: {total}")
    return total


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)


TEST_INPUT = [line.strip() for line in """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".split("\n") if line.strip()]

def test_find_mult_indexes():
    assert find_mult_indexes(TEST_INPUT[0]) == []
    assert find_mult_indexes(TEST_INPUT[1]) == [3]
    assert find_mult_indexes(TEST_INPUT[2]) == []
    assert find_mult_indexes(TEST_INPUT[3]) == []
    assert find_mult_indexes(TEST_INPUT[4]) == [3]
    assert find_mult_indexes(TEST_INPUT[5]) == []
    assert find_mult_indexes(TEST_INPUT[6]) == []
    assert find_mult_indexes(TEST_INPUT[7]) == []
    assert find_mult_indexes(TEST_INPUT[8]) == [5]
    assert find_mult_indexes(TEST_INPUT[9]) == []

def test_find_adjacent_numbers():
    assert find_adjacent_numbers(None, TEST_INPUT[1], TEST_INPUT[2], 3) == [35]
    assert find_adjacent_numbers(TEST_INPUT[0], TEST_INPUT[1], TEST_INPUT[2], 3) == [467, 35]
    assert find_adjacent_numbers(TEST_INPUT[0], TEST_INPUT[1], None, 3) == [467]

def test_input():
    assert main(None) == 91031374
