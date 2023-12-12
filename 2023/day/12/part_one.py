import re
from collections.abc import Iterator
from contextlib import suppress
from functools import cache
from typing import Any
from typing import Optional

from loguru import logger

from part_zero import Input
from part_zero import PartZero
from part_zero import Prompt

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")


class Row:
    def __init__(self, springs: str, damages: tuple[int, ...]):
        self.springs = springs
        self.damages = damages

    @cache
    def generate_pattern(self, damage: int) -> str:
        return r"^[^#]*?([#\?]{%s})(?:[^#]|$)" % damage

    @cache
    def count_solutions(
        self, line: Optional[str] = None, damages: Optional[tuple[int, ...]] = None
    ) -> int:
        if line is None:
            line = self.springs
            damages = self.damages

        if not damages:
            return "#" not in line

        pattern = self.generate_pattern(damages[0])

        count = 0
        if match := re.search(pattern, line):
            start, end = match.span(1)

            new_line = line[end + 1 :]
            count += self.count_solutions(new_line, damages[1:])

            if match.group(1).startswith("?"):
                new_line = line[start:].replace("?", ".", 1)
                count += self.count_solutions(new_line, damages)
        return count


class Record:
    def __init__(self, rows: list[Row]):
        self.rows = rows

    def __iter__(self) -> Iterator[Row]:
        return iter(self.rows)


class PartOne(PartZero):
    @staticmethod
    def parse_line(line: str) -> Row:
        springs, damaged = line.split(" ")
        return Row(springs, tuple(map(int, damaged.split(","))))

    @classmethod
    def parse(cls, input: Input) -> Any:
        return Record(list(map(cls.parse_line, iter(input))))

    @staticmethod
    def process(parsed_input: Any) -> int:  # type: ignore
        record: Record = parsed_input
        return sum(map(lambda r: r.count_solutions(), iter(record)))


class PartTwo(PartOne):
    @staticmethod
    def parse_line(line: str) -> Row:
        springs, damaged = line.split(" ")
        damaged_tuple = tuple(map(int, damaged.split(",")))
        return Row("?".join([springs] * 5), damaged_tuple * 5)


test_input = Input("./test_input")
real_input = Input("./input")


def main() -> Iterator[bool]:
    yield PartOne.solve(Prompt(test_input, expected=21))
    yield PartOne.solve(Prompt(real_input, expected=7118))
    yield PartTwo.solve(Prompt(test_input, expected=525_152))
    yield PartTwo.solve(Prompt(real_input, expected=7_030_194_981_795))


if __name__ == "__main__":
    all(main())


def test_results() -> None:
    assert all(main())
