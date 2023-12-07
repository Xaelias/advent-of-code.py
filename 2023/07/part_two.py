import os
import sys

from loguru import logger
from typing import Optional

from part_one import *


class HandPartTwo(Hand):
    CARDS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    def rank_hand(self):
        card_count_without_joker = sorted([v for k, v in self.counts.items() if k != "J"])
        if self.counts.get("J") == 5:
            # everything is a joker
            card_count_with_joker = [5]
        else:
            card_count_with_joker = card_count_without_joker
            card_count_with_joker[-1] += self.counts.get("J", 0)

        ranked_hand = next((hand for hand in valid_hands if hand.comp == card_count_with_joker))
        logger.debug(f"Ranked {self.cards} as {ranked_hand}")
        return ranked_hand


class PartTwo(PartOne):
    def parse(self) -> list[HandPartTwo]:
        hands = []
        for line in self.str():
            hand, bid = line.strip().split(" ")
            bid = int(bid)
            hands.append(HandPartTwo(hand, bid))
            logger.trace(f"Parsed {line=} into {hands[-1]=}")
        return hands

    def process(self) -> int:
        hands = self.parse()
        hands = sorted(hands)

        logger.debug(f"Sorted hands:")
        for hand in hands:
            logger.debug(repr(hand))

        return sum((i+1) * hands[i].bid for i in range(len(hands)))

class PartTwoExample(PartOneExample, PartTwo):
    pass


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartTwoExample().solve(5905)
    PartTwo(input).solve(245461700)

def test_compare_hands():
    better = Hand("KK677", 1)
    worse = Hand("KTJJT", 2)
    assert better > worse

def test_test_input():
    assert PartTwoExample().solve(5905)

def test_input():
    assert PartTwo(None).solve(245461700)

