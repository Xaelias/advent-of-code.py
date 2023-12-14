from collections.abc import Iterator
from contextlib import suppress
from typing import Annotated
from typing import Literal
from typing import Optional
from typing import Union

import numpy as np
import numpy.typing as npt
from loguru import logger
from part_zero import Input
from part_zero import PartZero
from part_zero import Prompt

ArrayNxM = Annotated[npt.NDArray[Union[bool | str]], Literal["N", "N"]]

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")
"""
    5║
.#..#║#..#
##.#.║.#.#
..###║###.
..###║###.
##.#.║.#.#
##..#║#..#
.#.#.║.#.#
    5║

  .###..##.
  .####.##.
  ##..##...
4 .....#..# 4
═════════════
  .....#..#
  ##..##...
  .####.##.
"""


def pprint(
    mirror: ArrayNxM,
    log_level="INFO",
    v_line: Optional[list[int]] = None,
    h_line: Optional[list[int]] = None,
) -> None:
    v_line = [] if v_line is None else v_line
    h_line = [] if h_line is None else h_line

    header_height = len(str(max(v_line) + 1)) if v_line else 0
    # +1 to make it more readable
    margin_width = 1 + len(str(max(h_line) + 1)) if h_line else 0
    width = len(mirror[0]) + margin_width * 2
    height = len(mirror) + header_height * 2

    printable_mirror = np.full((height, width), " ")
    printable_mirror[
        header_height : header_height + len(mirror), margin_width : margin_width + len(mirror[0])
    ] = mirror

    # pre-compute the human readable values
    v_line = [v + 1 for v in v_line]
    h_line = [h + 1 for h in h_line]

    for idx, h in enumerate(h_line):
        idx = header_height + idx + h
        # insert a new line full of ═ where the symmetry exists
        printable_mirror = np.insert(printable_mirror, idx, "═", axis=0)
        # insert the human readable row number on left and right (above axis)
        printable_mirror[idx - 1, :margin_width] = list(str(h).ljust(margin_width))
        printable_mirror[idx - 1, -margin_width:] = list(str(h).rjust(margin_width))

    # NB this doesnt account for ╬ where 2 axis would meet since the problem only deals with 1
    # summetry at a time
    for idx, v in enumerate(v_line):
        idx = margin_width + idx + v
        # insert a new column full of ║ where the symmetry exists
        printable_mirror = np.insert(printable_mirror, idx, "║", axis=1)
        # insert the human readable colum number at the top and bottom (left of the axis)
        printable_mirror[:header_height, idx - 1] = np.transpose(list(str(v).ljust(header_height)))
        printable_mirror[-header_height:, idx - 1] = np.transpose(list(str(v).ljust(header_height)))

    for row in printable_mirror:
        logger.log(log_level, "".join(["." if c == "T" else "#" if c == "F" else c for c in row]))

    # empty line for readability
    logger.log(log_level, "")


def check_if_mirrored(mirror: ArrayNxM, axis: int, vertical: bool) -> int:
    # if looking at a vertical axis transpose just to make my life easier
    if vertical:
        mirror = np.transpose(mirror)

    # the limit would be _after_ the ID passed to this function
    idx = axis + 1
    # we only consider an equal number of rows on each side, without leaving the original pattern
    size = min(idx, mirror.shape[0] - idx)

    # slice the original mirror and reverse the left side
    left = mirror[idx - size : idx][::-1]
    right = mirror[idx : idx + size]

    assert left.size == right.size  # just in case

    return left.size - sum([np.count_nonzero(a == b) for a, b in zip(left, right)])


class PartOne(PartZero):
    @classmethod
    def parse(cls, input: Input) -> list[ArrayNxM]:
        mirrors = []
        for mirror in input.split_on_empty_lines():
            mirrors.append(
                # store as True / False, doesnt matter which except for ``pprint``
                np.array([[c == "#" for c in line] for line in mirror])
            )
        return mirrors

    @classmethod
    def process_mirror(cls, mirror: ArrayNxM) -> int:
        for i in range(mirror.shape[0] - 1):
            value = check_if_mirrored(mirror, i, vertical=False)
            if value == 0:
                points = (i + 1) * 100
                logger.debug(
                    f"Mirror is flipped horizontally between {i+1} and {i+2} ({points} points)."
                )
                pprint(mirror, h_line=[i])
                return points
        else:
            # same but other direction
            for j in range(mirror.shape[1] - 1):
                value = check_if_mirrored(mirror, j, vertical=True)
                if value == 0:
                    points = j + 1
                    logger.debug(
                        f"Mirror is flipped vertically between {j+1} and {j+2} ({points} point(s))."
                    )
                    pprint(mirror, v_line=[j])
                    return points
        return 0  # just in case there is no symmetry

    @classmethod
    def process(cls, parsed_input: list[ArrayNxM]) -> int:  # type: ignore
        return sum(map(cls.process_mirror, parsed_input))


class PartTwo(PartOne):
    @classmethod
    def process_mirror(cls, mirror: ArrayNxM) -> int:
        # we need to ignore the original symmetry axis
        previous_points = super().process_mirror(mirror)
        for i in range(mirror.shape[0] - 1):
            value = check_if_mirrored(mirror, i, vertical=False)
            # we need exactly 1 difference
            if value == 1:
                points = (i + 1) * 100
                if points == previous_points:
                    continue
                logger.debug(
                    f"Mirror is flipped horizontally between {i+1} and {i+2} ({points} points)."
                )
                pprint(mirror, h_line=[i])
                return points
        else:
            # same but other direction
            for j in range(mirror.shape[1] - 1):
                value = check_if_mirrored(mirror, j, vertical=True)
                if value == 1:
                    points = j + 1
                    if points == previous_points:
                        continue
                    logger.debug(
                        f"Mirror is flipped vertically between {j+1} and {j+2} ({points} point(s))."
                    )
                    pprint(mirror, v_line=[j])
                    return points
        return 0


test_input = Input("./test_input")
real_input = Input("./input")


def main() -> Iterator[bool]:
    yield PartOne.solve(Prompt(test_input, expected=405))
    yield PartOne.solve(Prompt(real_input, expected=37_975))
    yield PartTwo.solve(Prompt(test_input, expected=4_00))
    yield PartTwo.solve(Prompt(real_input, expected=32_497))


if __name__ == "__main__":
    all(main())


def test_results() -> None:
    assert all(main())
