import math
import os
import sys

from loguru import logger
from typing import Optional

from part_one import *

TEST_INPUT_RESULT = 6
REAL_INPUT_RESULT = 20220305520997


class PartTwo(PartOne):
    def process(self) -> int:
        _, maps = self.parse()
        _process = super().process
        l = seq((m for m in maps if m.endswith("A"))).map(lambda start: _process(start=start, end="Z"))
        return math.lcm(*l)


class PartTwoExample(PartOneExample, PartTwo):
    default_input = "./test_input_3"


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartTwoExample().solve(TEST_INPUT_RESULT)
    PartTwo(input).solve(REAL_INPUT_RESULT)

def test_test_input():
    assert PartTwoExample().solve(TEST_INPUT_RESULT)

def test_input():
    assert PartTwo().solve(REAL_INPUT_RESULT)

