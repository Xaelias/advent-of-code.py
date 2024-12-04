import os
from collections import OrderedDict
from collections.abc import Iterable
from collections.abc import Iterator
from dataclasses import dataclass

from aocl.base import AoCInput
from aocl.base import Base


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


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[str]:
        return input_data.raw.split(",")

    @classmethod
    def process_part_one(cls, parsed_input: list[str], **kwargs) -> int:
        return sum(hash(string) for string in parsed_input)

    @classmethod
    def process_part_two(cls, parsed_input: list[str], **kwargs) -> int:
        boxes = Boxes(256)
        any(map(boxes.swap_lens, parsed_input))
        return sum(list(map(Box.focus_power, (box for box in boxes))))


def main() -> None:
    _, year, _, day = os.path.dirname(__file__).rsplit("/", maxsplit=3)
    Solution(year=year, day=day).solve_all()


if __name__ == "__main__":
    main()
