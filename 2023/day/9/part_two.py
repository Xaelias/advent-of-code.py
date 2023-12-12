import sys

from loguru import logger

from part_one import *

TEST_INPUT_RESULT = 2
REAL_INPUT_RESULT = 933


class PartTwo(PartOne):
    def process(self) -> int:
        return self.as_seq.map(self.parse_line).map(lambda x: self.reduce(x, index=0, sign=-1)).sum()

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
