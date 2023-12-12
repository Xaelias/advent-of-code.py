import sys

from loguru import logger

from part_one import *

TEST_INPUT_RESULT = 45000
REAL_INPUT_RESULT = 207576


class PartTwo(PartOne):
    def process(self) -> int:
        l = self.parse()
        return seq(l).map(sum).sorted(reverse=True).take(3).sum()

class PartTwoExample(PartOneExample, PartTwo):
    pass


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    PartTwoExample().solve(TEST_INPUT_RESULT)
    PartTwo(input).solve(REAL_INPUT_RESULT)

def test_test_input__part_two():
    assert PartTwoExample().solve(TEST_INPUT_RESULT)

def test_real_input__part_two():
    assert PartTwo().solve(REAL_INPUT_RESULT)
