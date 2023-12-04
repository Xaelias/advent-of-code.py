#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur
# Date              : 2023/12/04 16:02:12
# Last Modified Date: 2023/12/04 16:39:29
# Last Modified By  : Alexis Lesieur
from collections import namedtuple
from loguru import logger

import os
import re
import sys


Card = namedtuple("card", ["id", "winning", "numbers", "matches", "count"])
class Card:
    def __init__(self, id: int, winning: list[int], numbers: list[int]):
        self.id = id
        self.winning = winning
        self.numbers = numbers

        self.matches = len(winning & numbers)
        self.count = 1

    def increase(self, count: int):
        self.count += count

    def __str__(self):
        return f"{self.id}: count={self.count}, winning numbers={self.matches}"

    def __repr__(self):
        return f"Card<{self}>"


def parse_line(line: str) -> Card:
    logger.debug(f"Processing line. [{line=}]")
    card, winning, numbers = re.split(r"(?:: | \| )", line)
    logger.trace(f"Split input. [{line=}, {card=}, {winning=}, {numbers=}]")
    card = int(card[len("Card "):])
    winning = {int(e) for e in re.split(r" +", winning) if e}
    logger.trace(f"Extraced winning numbers. [{line=}, {winning=}]")
    numbers = {int(e) for e in re.split(r" +", numbers) if e}
    logger.trace(f"Extraced my numbers. [{line=}, {numbers=}]")

    return Card(
        id=card,
        winning=winning,
        numbers=numbers,
    )


def process_input(iterable) -> int:
    data = [parse_line(line) for line in iterable]

    running_total = 0
    index = -1

    while (index := index + 1) < len(data):
        card = data[index]
        logger.debug(f"Processing card. [{card=}]")

        running_total += card.count
        for i in range(index+1, index+1+card.matches):
            data[i].increase(card.count)
            logger.debug(f"Winning {card.count}×{data[i]!r}")

    return running_total, data


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./input")
    possible_games = []
    with open(input, "r") as f:
        total, _ = process_input((line.strip() for line in f.readlines()))
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
    assert parse_line(TEST_INPUT[0]).matches == 4
    assert parse_line(TEST_INPUT[1]).matches == 2
    assert parse_line(TEST_INPUT[2]).matches == 2
    assert parse_line(TEST_INPUT[3]).matches == 1
    assert parse_line(TEST_INPUT[4]).matches == 0
    assert parse_line(TEST_INPUT[5]).matches == 0


def test_test_input():
    total, data = process_input(TEST_INPUT)
    assert total == 30
    assert data[0].count == 1
    assert data[1].count == 2
    assert data[2].count == 4
    assert data[3].count == 8
    assert data[4].count == 14
    assert data[5].count == 1

def test_part_one():
    assert main(None) == 8736438
