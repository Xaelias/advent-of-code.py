#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur <Me@ALesieur.net>
# Date              : 2023/12/03 08:58:22
# Last Modified Date: 2023/12/03 11:04:53
# Last Modified By  : Alexis Lesieur <Me@ALesieur.net>
from loguru import logger
from typing import Optional

import os
import re
import sys


digits = [str(d) for d in range(0, 10)]


def find_symbols_indexes(line: str) -> list[int]:
    return [match.start() for match in re.finditer(r"[^\d\.]", line)]


def extract_number_at_index(line: str, index: int) -> Optional[int]:
    logger.trace(f"Trying to extract numbers from {line=} at {index=}.")

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
    previous_line = ""

    previous_symbols = []
    results = []
    for line in iterable:
        logger.trace(f"Processing new line: {line=}")
        numbers, new_symbols, cleaned_line = process_line(line, previous_symbols)
        results.extend(numbers)

        if previous_line:
            logger.trace(f"Processing previous line with new symbols.")
            numbers, _, _ = process_line(previous_line, new_symbols)
            results.extend(numbers)

        previous_line = cleaned_line
        previous_symbols = new_symbols
    return sum(results)



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

def test_find_symbols_indexes_test_data():
    assert find_symbols_indexes(TEST_INPUT[0]) == []
    assert find_symbols_indexes(TEST_INPUT[1]) == [3]
    assert find_symbols_indexes(TEST_INPUT[2]) == []
    assert find_symbols_indexes(TEST_INPUT[3]) == [6]
    assert find_symbols_indexes(TEST_INPUT[4]) == [3]
    assert find_symbols_indexes(TEST_INPUT[5]) == [5]
    assert find_symbols_indexes(TEST_INPUT[6]) == []
    assert find_symbols_indexes(TEST_INPUT[7]) == []
    assert find_symbols_indexes(TEST_INPUT[8]) == [3, 5]
    assert find_symbols_indexes(TEST_INPUT[9]) == []

def test_extract_number_at_index():
    assert extract_number_at_index(TEST_INPUT[0], 0) == (467, ".....114..")
    assert extract_number_at_index(TEST_INPUT[0], 1) == (467, ".....114..")
    assert extract_number_at_index(TEST_INPUT[0], 2) == (467, ".....114..")
    assert extract_number_at_index(TEST_INPUT[0], 3) == (None, TEST_INPUT[0])
    assert extract_number_at_index(TEST_INPUT[0], 4) == (None, TEST_INPUT[0])
    assert extract_number_at_index(TEST_INPUT[0], 5) == (114, "467.......")
    assert extract_number_at_index(TEST_INPUT[0], 6) == (114, "467.......")
    assert extract_number_at_index(TEST_INPUT[0], 7) == (114, "467.......")
    assert extract_number_at_index(TEST_INPUT[0], 8) == (None, TEST_INPUT[0])
    assert extract_number_at_index(TEST_INPUT[0], 9) == (None, TEST_INPUT[0])

    # edge case
    assert extract_number_at_index("....100000", 9) == (100000, "..........")

def test_process_line():
    assert process_line(TEST_INPUT[0], []) == ([], [], TEST_INPUT[0])
    assert process_line(TEST_INPUT[1], []) == ([], [3], TEST_INPUT[1])
    assert process_line(TEST_INPUT[0], [3]) == ([467], [], ".....114..")

def test_process_input():
    assert process_input(TEST_INPUT) == 4361

def test_part_one():
    assert main(None) == 546563
