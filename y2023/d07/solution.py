from dataclasses import dataclass
from typing import Any

from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base


@dataclass(frozen=True)
class ValidHand:
    name: str
    value: int
    comp: tuple[int, ...]


valid_hands = {
    ValidHand(name="Five of a Kind", value=7, comp=(5,)),
    ValidHand(name="Four of a Kind", value=6, comp=(1, 4)),
    ValidHand(name="Full House", value=5, comp=(2, 3)),
    ValidHand(name="Three of a Kind", value=4, comp=(1, 1, 3)),
    ValidHand(name="Two Pairs", value=3, comp=(1, 2, 2)),
    ValidHand(name="One Pair", value=2, comp=(1, 1, 1, 2)),
    ValidHand(name="High Card", value=1, comp=(1, 1, 1, 1, 1)),
}


class Hand:
    CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    def __init__(self, cards: str, bid: int):
        self.cards = list(cards)
        self.counts = self.count_cards()
        self.hand_shape = tuple(sorted(self.counts.values()))
        self.bid = bid
        self.rank = self.rank_hand()

    def count_cards(self) -> dict[str, int]:
        return {k: self.cards.count(k) for k in set(self.cards)}

    def rank_hand(self):
        ranked_hand = next((hand for hand in valid_hands if hand.comp == self.hand_shape))
        return ranked_hand

    def __eq__(self, other) -> bool:
        r = self.cards == other.cards and self.counts == other.counts
        return r

    def __gt__(self, other) -> bool:
        if self.rank.value > other.rank.value:
            return True
        if self.rank.value < other.rank.value:
            return False
        for s, o in zip(self.cards, other.cards):
            if s == o:
                continue
            r = self.CARDS.index(s) < self.CARDS.index(o)
            return r
        return False


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

        ranked_hand = next(
            (hand for hand in valid_hands if hand.comp == tuple(card_count_with_joker))
        )
        logger.debug(f"Ranked {self.cards} as {ranked_hand}")
        return ranked_hand


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        hands = []
        for line in input_data.as_list_of_str:
            hand, bid = line.strip().split(" ")
            hands.append(Hand(hand, int(bid)))
            logger.trace(f"Parsed {line=} into {hands[-1]=}")
        return sorted(hands)

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        hands = parsed_input
        return sum((i + 1) * hands[i].bid for i in range(len(hands)))

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        hands = []
        for line in input_data.as_list_of_str:
            hand, bid = line.strip().split(" ")
            hands.append(HandPartTwo(hand, int(bid)))
            logger.trace(f"Parsed {line=} into {hands[-1]=}")
        return sorted(hands)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        return cls.process_part_one(parsed_input, **kwargs)
