from typing import Any

from functional import seq
from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base

UP = 1
DOWN = -1
MIN_SPREAD = 1
MAX_SPREAD = 3


def is_step_safe(first: int, second: int, direction: int) -> bool:
    safe = MIN_SPREAD <= direction * (second - first) <= MAX_SPREAD
    logger.trace(f"returned True [{first=}, {second=}, {direction=}]")
    return safe


def is_report_safe(report: list[int]) -> bool:
    safe = is_report_safe_rec(report)
    logger.debug(f"returned {safe} [{report=}]")
    return safe


def is_report_safe_rec(report: list[int], idx: int = 0, direction: int | None = None) -> bool:
    try:
        first = report[idx]
        second = report[idx + 1]
        if direction is None:
            direction = get_direction(first, second)
        return is_step_safe(
            first,
            second,
            direction,
        ) and is_report_safe_rec(
            report,
            idx + 1,
            direction,
        )
    except IndexError:
        return True


def is_report_safe_part_two(
    report: list[int],
    authorized_failures: int = 1,
) -> bool:
    safe = is_report_safe_part_two_rec(report, authorized_failures=authorized_failures)
    logger.debug(f"returned {safe} [{report=}, {authorized_failures=}]")
    return safe


def is_report_safe_part_two_rec(
    report: list[int],
    first_idx: int = 0,
    second_idx: int = 1,
    direction: int | None = None,
    authorized_failures: int = 1,
) -> bool:
    if authorized_failures < 0:
        logger.trace(
            f"returned False [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
        )
        return False

    if second_idx >= len(report):
        logger.trace(
            f"returned True [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
        )
        return True

    try:
        first = report[first_idx]
        second = report[second_idx]
        if direction is None:
            direction = get_direction(first, second)
        step_is_safe = is_step_safe(
            first,
            second,
            direction,
        )

        if step_is_safe:
            if authorized_failures == 0:
                safe = is_report_safe_rec(report, second_idx, direction)
                logger.trace(
                    f"returned {safe} [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
                )
                return safe

            safe = is_report_safe_part_two_rec(
                report,
                first_idx=second_idx,
                second_idx=second_idx + 1,
                direction=direction,
                authorized_failures=authorized_failures,
            )
            logger.trace(
                f"returned {safe} [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
            )
            return safe

        # skip previous number
        #   X need to skip
        #     | error found
        # 4 5 3 2
        if first_idx >= 2:
            if is_report_safe_part_two_rec(
                report,
                first_idx=first_idx - 2,
                second_idx=first_idx,
                direction=None if first_idx == 2 else direction,
                authorized_failures=authorized_failures - 1,
            ):
                logger.trace(
                    f"returned True [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
                )
                return True

        # skip current/first number
        #   X need to skip
        #   } error found
        # 4 5 3 2 1
        if first_idx >= 1:
            if is_report_safe_part_two_rec(
                report,
                first_idx=first_idx - 1,
                second_idx=first_idx + 1,
                direction=None if first_idx == 1 else direction,
                authorized_failures=authorized_failures - 1,
            ):
                logger.trace(
                    f"returned True [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
                )
                return True

        # we need to add a couple special cases
        if first_idx == 0:
            # 99 1 2 3
            if is_report_safe_part_two_rec(
                report,
                first_idx=first_idx + 1,
                second_idx=first_idx + 2,
                direction=None,
                authorized_failures=authorized_failures - 1,
            ):
                logger.trace(
                    f"returned True [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
                )
                return True

        if first_idx == 1:
            # 67, 70, 67, 65, 64
            if is_report_safe_part_two_rec(
                report,
                first_idx=first_idx,
                second_idx=first_idx + 1,
                direction=None,
                authorized_failures=authorized_failures - 1,
            ):
                logger.trace(
                    f"returned True [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
                )
                return True

        # skip second
        safe = is_report_safe_part_two_rec(
            report,
            first_idx=first_idx,
            second_idx=first_idx + 2,
            direction=None if first_idx == 0 else direction,
            authorized_failures=authorized_failures - 1,
        )
        logger.trace(
            f"returned {safe} [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
        )
        return safe

    except IndexError:
        logger.trace(
            f"returned True [{report=}, {first_idx=}, {second_idx=}, {direction=}, {authorized_failures=}]"
        )
        return True


def get_direction(first: int, second: int) -> int:
    if second > first:
        return UP
    elif second < first:
        return DOWN
    else:  # first == second
        return 0


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[list[int]]:
        return [[int(c) for c in e.split()] for e in input_data.as_list_of_str]

    @classmethod
    def process_part_one(cls, parsed_input: list[list[int]], **kwargs: Any) -> int:
        return seq(parsed_input).map(is_report_safe).sum()

    @classmethod
    def process_part_two(cls, parsed_input: list[list[str]], **kwargs: Any) -> int:
        return seq(parsed_input).map(is_report_safe_part_two).sum()
