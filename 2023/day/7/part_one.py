import os
import re
import sys

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from loguru import logger
from typing import Optional

logger.level("FAILED", no=41, color="<red>")


class ValidHand:
    def __init__(self, name: str, value: int, comp: list[int]):
        self.name = name
        self.value = value
        self.comp = comp

    def __repr__(self) -> str:
        return f"<ValidHand {self.name} (value={self.value})>"


valid_hands = {
    ValidHand(name="Five of a Kind", value=7, comp=[5]),
    ValidHand(name="Four of a Kind", value=6, comp=[1, 4]),
    ValidHand(name="Full House", value=5, comp=[2, 3]),
    ValidHand(name="Three of a Kind", value=4, comp=[1, 1, 3]),
    ValidHand(name="Two Pairs", value=3, comp=[1, 2, 2]),
    ValidHand(name="One Pair", value=2, comp=[1, 1, 1, 2]),
    ValidHand(name="High Card", value=1, comp=[1, 1, 1, 1, 1]),
}

class Hand:
    CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    def __init__(self, cards: str, bid: int):
        cards = list(cards)
        self.cards = cards
        self.counts = self.count_cards()
        self.bid = bid
        self.rank = self.rank_hand()

    def __str__(self):
        return f"<{self.__class__.__name__}: {''.join(self.cards)}>"

    def __repr__(self):
        return f"<{self.__class__.__name__}: cards={''.join(self.cards)}, counts={self.counts}, bid={self.bid}, {self.rank}>"

    def count_cards(self) -> dict[str, int]:
        return {k: self.cards.count(k) for k in set(self.cards)}

    def rank_hand(self):
        ranked_hand = next((hand for hand in valid_hands if hand.comp == sorted(self.counts.values())))
        logger.debug(f"Ranked {self.cards} as {ranked_hand}")
        return ranked_hand

    def __eq__(self, other) -> bool:
        r = self.cards == other.cards and self.counts == other.counts
        logger.trace(f"{self} == {other} == {r}")
        return r

    def __gt__(self, other) -> bool:
        if self.rank.value > other.rank.value:
            logger.trace(f"{self} > {other} == True because {self.rank.name} > {other.rank.name}")
            return True
        if self.rank.value < other.rank.value:
            logger.trace(f"{self} > {other} == False because {self.rank.name} < {other.rank.name}")
            return False
        for s, o in zip(self.cards, other.cards):
            if s == o:
                continue
            r = self.CARDS.index(s) < self.CARDS.index(o)
            logger.trace(f"{self} > {other} == {r} because {s} > {o}")
            return r
        logger.trace(f"{self} > {other} == False")
        return False


class Main(ABC):
    def str(self) -> list[str]:
        with open(self.input, "r") as f:
            return f.readlines()

    def iter(self) -> Iterable[str]:
        return iter(self.str())

    @abstractmethod
    def parse(self) -> list[Hand]:
        ...

    @abstractmethod
    def process(self) -> int:
        ...

    def solve(self, expected: Optional[int]=None) -> bool:
        solution = self.process()
        if expected is not None:
            if solution == expected:
                logger.success(f"Solution for {self.__class__.__name__}: {solution:,d} ({solution}).")
            else:
                logger.log("FAILED", f"Expected solution for {self.__class__.__name__} to be {expected:,d} but found {solution:,d}.")
        else:
            logger.warning(f"Solution for {self.__class__.__name__}: {solution:,d} ({solution}). No expected value provided.")
        return solution == expected


class PartOne(Main):
    def __init__(self, input: Optional[str]=None):
         self.input = input or os.path.join(os.path.dirname(__file__), "./input")

    def parse(self) -> list[Hand]:
        hands = []
        for line in self.str():
            hand, bid = line.strip().split(" ")
            bid = int(bid)
            hands.append(Hand(hand, bid))
            logger.trace(f"Parsed {line=} into {hands[-1]=}")
        return hands

    def process(self) -> int:
        hands = self.parse()
        hands = sorted(hands)

        logger.debug(f"Sorted hands:")
        for hand in hands:
            logger.debug(repr(hand))

        return sum((i+1) * hands[i].bid for i in range(len(hands)))


class PartOneExample(PartOne):
    def __init__(self, input: Optional[str]=None):
         self.input = input or os.path.join(os.path.dirname(__file__), "./test_input")


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartOneExample().solve(6440)
    PartOne(input).solve(247823654)

def test_compare_hands():
    better = Hand("KK677", 1)
    worse = Hand("KTJJT", 2)
    assert better > worse

def test_test_input():
    assert PartOneExample().solve(6440)

def test_input():
    assert PartOne(None).solve(247823654)
