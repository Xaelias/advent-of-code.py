from contextlib import suppress
from enum import Enum
from loguru import logger

import os
import sys
import regex as re

# logger.add(sys.stderr, serialize=True)
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>{extra[str_representation]}"
)
logger = logger.patch(lambda record: record["extra"].update(str_representation=f" [{', '.join(f'{k}={v!r}' for k, v in record['extra'].items())}]" if record['extra'] else ''))
logger.remove()
logger.add(sys.stderr, format=logger_format)


class Numbers(Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
    seven = "7"
    eight = "8"
    nine = "9"


PATTERN = rf"[0-9]|{'|'.join(n.name for n in Numbers)}"


def find_first_and_last_number_spelled(line: str) -> int:
    numbers = re.finditer(PATTERN, line, overlapped=True)
    first_m = next(numbers)
    try:
        *_, last_m = numbers
    except Exception:
        last_m = first_m

    first = first_m.group(0)
    last = last_m.group(0)

    with suppress(KeyError):
        first = Numbers[first].value
    with suppress(KeyError):
        last = Numbers[last].value

    total = int(first + last)
    logger.bind(line=line, first=first_m.group(0), last=last_m.group(0), total=total).debug("Processed line.")

    return total


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./0_input")
    with open(input, "r") as f:
        total = sum((find_first_and_last_number_spelled(line.strip()) for line in f.readlines()), 0)
    logger.info(f"The total for the dataset is: {total}")
    return total


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)


def test_provided_first_part():
    assert find_first_and_last_number_spelled("1abc2") == 12
    assert find_first_and_last_number_spelled("pqr3stu8vwx") == 38
    assert find_first_and_last_number_spelled("a1b2c3d4e5f") == 15
    assert find_first_and_last_number_spelled("treb7uchet") == 77


def test_provided():
    assert find_first_and_last_number_spelled("two1nine") == 29
    assert find_first_and_last_number_spelled("eightwothree") == 83
    assert find_first_and_last_number_spelled("abcone2threexyz") == 13
    assert find_first_and_last_number_spelled("xtwone3four") == 24
    assert find_first_and_last_number_spelled("4nineeightseven2") == 42
    assert find_first_and_last_number_spelled("zoneight234") == 14
    assert find_first_and_last_number_spelled("7pqrstsixteen") == 76


def test_edge_case():
    assert find_first_and_last_number_spelled("twone") == 21


def test_real():
    assert main(None) == 55358
