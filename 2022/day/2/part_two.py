import sys

from loguru import logger

from part_one import *

TEST_INPUT_RESULT = 12
REAL_INPUT_RESULT = 12424


class PartTwo(PartOne):
    def parse_line(self, line: str) -> tuple[Shape, str]:
        return (Shape.convert(line[0]), line[2])

    def process(self) -> int:
        return (
            self.as_seq
                .map(self.parse_line)
                .starmap(
                    lambda x, y: self.find_correct_move(x, y).mine_against(x)
                ).sum()
        )

    def find_correct_move(self, their: Shape, result: str) -> Shape:
        match result:
            case "X":
                # I should lose
                return their.win_against()
            case "Y":
                # draw
                return their.__class__()
            case "Z":
                # I should win
                return their.lose_against()

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
