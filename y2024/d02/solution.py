from typing import Any

from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import yd
from aocl.base import yt


def abs_diff(input: tuple[str, str]) -> int:
    return abs(int(input[1]) - int(input[0]))


@yt(show_enter=False)
def is_report_safe(
    report: list[int],
    min_spread: int = 1,
    max_spread: int = 3,
    increasing: bool | None = None,
) -> bool:
    if len(report) <= 1:
        return True

    first, *remainder = report

    if increasing is None:
        increasing = first <= remainder[0]

    second = remainder[0]
    if (increasing and second < first) or (not increasing and first < second):
        yt(first, second, increasing)
        return False
    if not (min_spread <= abs(first - second) <= max_spread):
        yt(first, second, min_spread, max_spread)
        return False

    return is_report_safe(
        report=remainder,
        increasing=increasing,
        min_spread=min_spread,
        max_spread=max_spread,
    )


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[int]]:
        return [[int(c) for c in e.split()] for e in input_data.as_list_of_str]

    @classmethod
    def process_part_one(cls, parsed_input: list[list[int]], **kwargs: Any) -> int:
        yt(parsed_input)

        total = 0
        for report in parsed_input:
            safe = is_report_safe(report=report)
            yd(report, safe)
            total += safe
        return total

    @classmethod
    def process_part_two(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
        yt(parsed_input)

        total = 0
        for report in parsed_input:
            safe = is_report_safe(report=report)
            if not safe:
                for idx in range(len(report)):
                    new_report = report[::]
                    new_report.pop(idx)
                    safe = is_report_safe(report=new_report)
                    if safe:
                        break

            yd(report, safe)
            total += safe
        return total
