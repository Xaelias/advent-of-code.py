#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur
# Date              : 2023/12/04 17:05:23
# Last Modified Date: 2023/12/04 17:23:24
# Last Modified By  : Alexis Lesieur
from loguru import logger

import os
import re
import sys

# Card #: winning #      | numbers you have
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
def process_line(line: str) -> int:
    logger.debug(f"Processing line. [{line=}]")
    card, winning, numbers = re.split(r"(?:: | \| )", line)
    logger.trace(f"Split input. [{line=}, {card=}, {winning=}, {numbers=}]")
    card = int(card[len("Card "):])
    winning = {int(e) for e in re.split(r" +", winning) if e}
    logger.trace(f"Extraced winning numbers. [{line=}, {winning=}]")
    numbers = {int(e) for e in re.split(r" +", numbers) if e}
    logger.trace(f"Extraced my numbers. [{line=}, {numbers=}]")

    matches = numbers & winning

    logger.info(f"Processed line. [Card {card}: {numbers=}, {winning=}, {matches=}]")
    return len(matches)

def process_input(iterable) -> int:
    to_add = []
    points = 0
    for line in iterable:
        matches = process_line(line)
        count = 1 + sum((count for count, _ in to_add))
        points += count
        logger.debug(f"Running score: {points}. [{to_add=}, {count=}]")
        to_add = [(count, for_next-1) for count, for_next in to_add if for_next > 1]
        if matches:
           to_add.append((count, matches))
    return points

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
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".split("\n") if line.strip()]



def test_process_line():
    assert process_line(TEST_INPUT[0]) == 4
    assert process_line(TEST_INPUT[1]) == 2
    assert process_line(TEST_INPUT[2]) == 2
    assert process_line(TEST_INPUT[3]) == 1
    assert process_line(TEST_INPUT[4]) == 0
    assert process_line(TEST_INPUT[5]) == 0


def test_test_input():
    assert process_input(TEST_INPUT) == 30

def test_full_input():
    assert main(None) == 8736438
