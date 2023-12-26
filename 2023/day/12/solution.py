import re
from collections.abc import Iterator
from functools import cache
from typing import Any
from typing import Optional

from aocl.base import AoCInput
from aocl.base import Base


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


class Solution(Base):
    @staticmethod
    def parse_line(line: str) -> Row:
        springs, damaged = line.split(" ")
        return Row(springs, tuple(map(int, damaged.split(","))))

    @classmethod
    def parse(cls, input_data: AoCInput) -> Record:
        return Record(list(map(cls.parse_line, input_data.as_list_of_str)))

    @classmethod
    def process_part_one(cls, parsed_input: Record, **kwargs: Any) -> int:
        return sum(map(lambda r: r.count_solutions(), iter(parsed_input)))

    @staticmethod
    def parse_line_part_two(line: str) -> Row:
        springs, damaged = line.split(" ")
        damaged_tuple = tuple(map(int, damaged.split(",")))
        return Row("?".join([springs] * 5), damaged_tuple * 5)

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Record:
        return Record(list(map(cls.parse_line_part_two, input_data.as_list_of_str)))

    @classmethod
    def process_part_two(cls, parsed_input: Record, **kwargs: Any) -> int:
        return sum(map(lambda r: r.count_solutions(), iter(parsed_input)))
