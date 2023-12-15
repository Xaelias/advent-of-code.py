from collections import OrderedDict
from collections.abc import Iterable
from collections.abc import Iterator
from contextlib import suppress
from dataclasses import dataclass

from loguru import logger
from part_zero import Input
from part_zero import PartZero
from part_zero import Prompt

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")


def hash(string: str) -> int:
    if not string:
        return 0
    return (hash(string[:-1]) + ord(string[-1])) * 17 % 256


@dataclass
class Box:
    idx: int
    lenses: dict[str, int]

    def focus_power(self) -> int:
        return sum(
            (
                (self.idx + 1) * (lens_id + 1) * lens_focus
                for lens_id, lens_label in enumerate(self.lenses)
                if (lens_focus := self.lenses[lens_label])
            )
        )

    def __getitem__(self, key: str) -> int:
        return self.lenses[key]

    def __setitem__(self, key: str, val: int) -> None:
        self.lenses[key] = val

    def pop(self, key):
        return self.lenses.pop(key, None)


class Boxes(Iterable):
    def __init__(self, size: int) -> None:
        self.boxes = [Box(i, OrderedDict()) for i in range(size)]

    def __iter__(self) -> Iterator[Box]:
        return iter(self.boxes)

    def swap_lens(self, operation: str) -> None:
        op = "=" if "=" in operation else "-"
        label, lens = operation.split(op)
        box_id = hash(label)
        box = self.boxes[box_id]

        if op == "-":
            box.pop(label)
        else:
            box[label] = int(lens)


class PartOne(PartZero):
    @classmethod
    def parse(cls, input: Input) -> list[str]:
        return input.as_str.strip().split(",")

    @classmethod
    def process(cls, parsed_input: list[str]) -> int:  # type: ignore
        return sum((hash(string) for string in parsed_input))


class PartTwo(PartOne):
    @classmethod
    def process(cls, parsed_input: list[str]) -> int:  # type: ignore
        boxes = Boxes(256)
        any(map(boxes.swap_lens, parsed_input))
        return sum(list(map(Box.focus_power, (box for box in boxes))))


test_input = Input("./test_input")
real_input = Input("./input")


def main() -> Iterator[bool]:
    HASH_hash = hash("HASH")
    assert HASH_hash == 52, f"{HASH_hash} != 52"
    yield PartOne.solve(Prompt(test_input, expected=1320))
    yield PartOne.solve(Prompt(real_input, expected=498538))
    yield PartTwo.solve(Prompt(test_input, expected=145))
    yield PartTwo.solve(Prompt(real_input, expected=286278))


if __name__ == "__main__":
    all(main())
