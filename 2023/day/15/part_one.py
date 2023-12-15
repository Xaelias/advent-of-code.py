from collections import OrderedDict
from collections.abc import Iterator
from contextlib import suppress

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


def focus_power(box_id: int, lenses: dict[str, int]) -> int:
    return sum(
        (
            (box_id + 1) * (lens_id + 1) * lens_focus
            for lens_id, lens_label in enumerate(lenses)
            if (lens_focus := lenses[lens_label])
        )
    )


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
        boxes: list[dict[str, int]] = [OrderedDict() for _ in range(256)]

        for chunk in parsed_input:
            operation = "=" if "=" in chunk else "-"
            label, lens = chunk.split(operation)
            box_id = hash(label)
            box = boxes[box_id]

            if operation == "-":
                box.pop(label, None)
            else:
                box[label] = int(lens)

        return sum((focus_power(idx, box) for idx, box in enumerate(boxes)))


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
