from abc import ABC
from abc import abstractmethod
from collections.abc import Iterator
from contextlib import suppress
from functools import cache
from typing import Any
from typing import Optional
from typing import Union

import numpy as np
from functional import seq
from functional.pipeline import Sequence
from loguru import logger

from aocl.parser import Puzzle

with suppress(Exception):
    logger.level("FAILED", no=25, color="<red>")


class AoCInput:
    def __init__(self, input_data: str) -> None:
        self.input_data = input_data

    def __eq__(self, other) -> bool:
        return self.input_data == other.input_data

    def __hash__(self) -> int:
        return hash(self.input_data)

    @property
    def raw(self) -> str:
        return self.input_data.strip()

    @property
    def as_chunks(self) -> list[list[str]]:
        return [[line.strip() for line in chunk.split()] for chunk in self.raw.split("\n\n")]

    @property
    def as_list_of_str(self) -> list[str]:
        return self.raw.split("\n")

    @property
    def as_seq(self) -> Sequence:
        return seq(self.as_list_of_str)

    @property
    def as_iter(self) -> Iterator[str]:
        return iter(self.as_list_of_str)

    @property
    def as_nparray(self):
        return np.array([list(row.strip()) for row in self.as_list_of_str])

    @property
    def as_list_of_nparray(self):
        return [np.array(chunk) for chunk in self.as_chunks]


class Base(ABC):
    def __init__(
        self,
        year: Union[int, str],
        day: Union[int, str],
        kwargs_part_one: Optional[dict[str, Any]] = None,
        kwargs_part_two: Optional[dict[str, Any]] = None,
        solve_part_one_examples: bool = True,
        solve_part_two_examples: bool = True,
        solve_part_one: bool = True,
        solve_part_two: bool = True,
        part_one_answer: Optional[str] = None,
        part_two_answer: Optional[str] = None,
        continue_on_failure: bool = False,
        data: Optional[str] = None,
    ):
        self.solve_part_one_examples = solve_part_one_examples
        self.solve_part_two_examples = solve_part_two_examples
        self.solve_part_one = solve_part_one
        self.solve_part_two = solve_part_two
        self.part_one_answer = part_one_answer
        self.part_two_answer = part_two_answer
        self.kwargs_part_one = kwargs_part_one or {}
        self.kwargs_part_two = kwargs_part_two or {}
        self.break_on_failure = not continue_on_failure
        self.data = data

        self.year = int(year)
        self.day = int(day)
        self.puzzle = Puzzle(
            year=self.year,
            day=self.day,
            data=data,
            answer_a=part_one_answer,
            answer_b=part_two_answer,
        )

    @classmethod
    @cache
    def cached_parse_part_one(cls, input_data: AoCInput) -> Any:
        return cls.parse(input_data)

    @classmethod
    @cache
    def cached_parse_part_two(cls, input_data: AoCInput) -> Any:
        return cls.parse_part_two(input_data)

    @classmethod
    @abstractmethod
    def parse(cls, input_data: AoCInput) -> Any:
        ...

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        return cls.cached_parse_part_one(input_data)

    @classmethod
    @abstractmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        ...

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        return cls.process_part_one(parsed_input, **kwargs)

    def solve_tests(self, part_id: int) -> tuple[int, int]:
        match part_id:
            case 1:
                prompt_list = "part_one"
                parse_fn = self.cached_parse_part_one
                process_fn = self.process_part_one
                part_name = "PartOne"
                kwargs = self.kwargs_part_one
            case 2:
                prompt_list = "part_two"
                parse_fn = self.cached_parse_part_two
                process_fn = self.process_part_two
                part_name = "PartTwo"
                kwargs = self.kwargs_part_two
            case _:
                raise ValueError(f"{part_id=} is not a valid part number.")

        example_id = 0
        failures = 0
        for example in self.puzzle.examples:
            for parameters in getattr(example, prompt_list):
                expected = parameters.answer
                if expected is not None:
                    example_id += 1
                    prefix = f"{part_name} Example #{example_id}"
                    suffix = f" ({parameters.kwargs})" if parameters.kwargs else ""
                    solution = process_fn(
                        parse_fn(AoCInput(example.input_data)),
                        **(parameters.kwargs or kwargs),
                    )
                    solution = str(solution)

                    if solution == expected:
                        logger.success(f"{prefix} - Found {solution}{suffix}")
                    else:
                        logger.log(
                            "FAILED", f"{prefix} - Found {solution} != expected {expected}{suffix}"
                        )
                        failures += 1
        return example_id - failures, failures

    def solve_reals(self, part_id: int) -> bool:
        match part_id:
            case 1:
                prompt_list = "part_one"
                parse_fn = self.cached_parse_part_one
                process_fn = self.process_part_one
                part_name = "PartOne"
                kwargs = self.kwargs_part_one
            case 2:
                prompt_list = "part_two"
                parse_fn = self.cached_parse_part_two
                process_fn = self.process_part_two
                part_name = "PartTwo"
                kwargs = self.kwargs_part_two
            case _:
                raise ValueError(f"{part_id=} is not a valid part number.")

        prompt = self.puzzle.prompt

        solution = process_fn(
            parse_fn(AoCInput(prompt.input_data)),
            **kwargs,
        )
        solution = str(solution)

        prefix = f"{part_name} Real Input"
        expected = getattr(prompt, prompt_list)[0].answer
        if expected is None:
            logger.warning(f"{prefix} - Found {solution} - no expected value provided.")
            return False
        elif solution == expected:
            logger.success(f"{prefix} - Found {solution}")
            return True
        else:
            logger.log("FAILED", f"{prefix} - Found {solution} != expected {expected}")
            return False

    def solve_all(self, skip_tests: bool = False):
        if self.solve_part_one_examples:
            if not self.solve_tests(1) and self.break_on_failure:
                return
        if self.solve_part_one:
            if not self.solve_reals(1) and self.break_on_failure:
                return
        if self.solve_part_two_examples:
            if not self.solve_tests(2) and self.break_on_failure:
                return
        if self.solve_part_two:
            if not self.solve_reals(2) and self.break_on_failure:
                return

    def get_answers(self) -> tuple[str, str]:
        try:
            answer_a = str(
                self.process_part_one(
                    self.cached_parse_part_one(AoCInput(self.puzzle.prompt.input_data)),
                    **self.kwargs_part_one,
                )
            )
        except Exception as e:
            answer_a = repr(e)
        try:
            answer_b = str(
                self.process_part_two(
                    self.cached_parse_part_two(AoCInput(self.puzzle.prompt.input_data)),
                    **self.kwargs_part_two,
                )
            )
        except Exception as e:
            answer_b = repr(e)
        return answer_a, answer_b
