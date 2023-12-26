import re
from typing import Any
from typing import Optional

from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base

digits = [str(d) for d in range(0, 10)]


def find_symbols_indexes(line: str) -> list[int]:
    return [match.start() for match in re.finditer(r"[^\d.]", line)]


def extract_number_at_index(line: str, index: int) -> tuple[Optional[int], str]:
    logger.trace(f"Trying to extract numbers from {line=} at {index=}.")

    if not line:
        logger.trace(f"Skipping empty line. [{line=}]")
        return None, line

    if index < 0:
        logger.trace(f"Skipping index < 0. [{line=}, {index=}]")
        return None, line

    if index >= len(line):
        logger.trace(f"Skipping index >= len(line). [{line=}, {len(line)=}, {index=}]")
        return None, line

    if line[index] in digits:
        logger.trace(f"Found a number! Extracting. [{line=}, {index=}, {line[index]=}]")
        s = line[index]

        i = 1
        while index - i >= 0 and line[index - i] in digits:
            s = line[index - i] + s
            i += 1
        start = index - i + 1
        i = 1
        while index + i < len(line) and line[index + i] in digits:
            s = s + line[index + i]
            i += 1
        end = index + i - 1

        number = int(s)
        new_line = line[0:start] + "." * len(s) + line[end + 1 :]
        logger.debug(f"Replaced found number with '.'s. [{line=}, {number=}, {new_line=}]")
        return number, new_line
    return None, line


def find_mult_indexes(line: str) -> list[int]:
    return [i for i in range(len(line)) if line[i] == "*"]


def find_adjacent_numbers(
    previous_line: Optional[str], current_line: str, next_line: Optional[str], index: int
) -> list[int]:
    numbers = []
    if previous_line:
        number, previous_line = extract_number_at_index(previous_line, index - 1)
        numbers.append(number)
        number, previous_line = extract_number_at_index(previous_line, index)
        numbers.append(number)
        number, previous_line = extract_number_at_index(previous_line, index + 1)
        numbers.append(number)

    number, current_line = extract_number_at_index(current_line, index - 1)
    numbers.append(number)
    number, current_line = extract_number_at_index(current_line, index)
    numbers.append(number)
    number, current_line = extract_number_at_index(current_line, index + 1)
    numbers.append(number)

    if next_line:
        number, next_line = extract_number_at_index(next_line, index - 1)
        numbers.append(number)
        number, next_line = extract_number_at_index(next_line, index)
        numbers.append(number)
        number, next_line = extract_number_at_index(next_line, index + 1)
        numbers.append(number)

    return [number for number in numbers if number is not None]


def process_line(line: str, provided_indexes: list[int]) -> tuple[list[int], list[int], str]:
    results = []

    my_symbols = find_symbols_indexes(line)
    logger.trace(f"Processing line self indexes. [{line=}, {my_symbols=}]")
    for symbol in my_symbols:
        number, line = extract_number_at_index(line, symbol - 1)
        if number:
            results.append(number)
        number, line = extract_number_at_index(line, symbol + 1)
        if number:
            results.append(number)

    logger.trace(f"Processing line with provided indexes. [{line=}, {provided_indexes=}].")
    for symbol in provided_indexes:
        number, line = extract_number_at_index(line, symbol - 1)
        if number:
            results.append(number)
            number = None
        else:
            number, line = extract_number_at_index(line, symbol)
        if number:
            results.append(number)
            number = None
        else:
            number, line = extract_number_at_index(line, symbol + 1)
        if number:
            results.append(number)
    return results, my_symbols, line


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return input_data.as_list_of_str

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        results = []

        previous_line = ""
        previous_symbols: list[int] = []
        for line in parsed_input:
            numbers, new_symbols, cleaned_line = process_line(line, previous_symbols)
            results.extend(numbers)

            if previous_line:
                numbers, _, _ = process_line(previous_line, new_symbols)
                results.extend(numbers)

            previous_line = cleaned_line
            previous_symbols = new_symbols
        return sum(results)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        current_line = None
        next_line = None
        total = 0
        for line in parsed_input:
            previous_line = current_line
            current_line = next_line
            next_line = line

            if current_line is None:
                continue

            mult_symbols = find_mult_indexes(current_line)
            for index in mult_symbols:
                numbers = find_adjacent_numbers(previous_line, current_line, next_line, index)
                if len(numbers) == 2:
                    total += numbers[0] * numbers[1]
        return total
