import json
import os
import re
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional

import git
from aocd.models import Puzzle as AoCPuzzle
from loguru import logger


@dataclass
class ProblemParameters:
    kwargs: dict[str, str] = field(default_factory=dict)
    answer: Optional[str] = field(default=None)


@dataclass
class Prompt:
    input_data: str = field(repr=False)
    part_one: list[ProblemParameters]
    part_two: list[ProblemParameters]


@dataclass
class Day(Prompt):
    examples: list[Prompt] = field(default_factory=list)


def get_git_root() -> str:
    git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


class Puzzle:
    # year: int
    # day: int
    # data: Optional[str]  # provided when calling aoc
    # part_one_examples: list[PartOneExample] = field(init=False, default_factory=list)
    # part_two_examples: list[PartTwoExample] = field(init=False, default_factory=list)
    # part_one_puzzle: Optional[PartOne] = field(init=False, default=None)
    # part_two_puzzle: Optional[PartTwo] = field(init=False, default=None)

    def __init__(
        self,
        year: int,
        day: int,
        data: Optional[str] = None,
        answer_a: Optional[str] = None,
        answer_b: Optional[str] = None,
    ) -> None:
        self.year = int(year)
        self.day = int(day)

        self.examples = []
        if data is not None:
            # we got data directly from the `aoc` command, just hardcode that and skip everything else
            self.prompt = Prompt(data, [], [])
            return

        git_root = get_git_root()
        self.test_input_file = f"y{self.year}/d{self.day:02}/test_input"
        self.real_input_file = f"y{self.year}/d{self.day:02}/input"

        self.aoc_puzzle = AoCPuzzle(year=self.year, day=self.day)

        try:
            with open(os.path.join(git_root, self.real_input_file), "r") as f:
                local_input_data = f.read().strip("\n")
            self.prompt = Prompt(
                input_data=local_input_data,
                part_one=[
                    ProblemParameters(answer=answer_a or getattr(self.aoc_puzzle, "answer_a", None))
                ],
                part_two=[
                    ProblemParameters(answer=answer_b or getattr(self.aoc_puzzle, "answer_b", None))
                ],
            )
        except Exception as e:
            logger.info("Using API data for main problems.")
            logger.trace(f"Failed to open/parse file. [{self.real_input_file}, {e=}]")
            self.prompt = Prompt(
                input_data=self.aoc_puzzle.input_data,
                part_one=[
                    ProblemParameters(answer=answer_a or getattr(self.aoc_puzzle, "answer_a", None))
                ],
                part_two=[
                    ProblemParameters(answer=answer_b or getattr(self.aoc_puzzle, "answer_b", None))
                ],
            )

        try:
            pattern = re.compile(r"-+ Example data [0-9]+/[0-9]+ -+")
            with open(os.path.join(git_root, self.test_input_file), "r") as f:
                local_test_input_data = f.read().strip("\n")
            _, *examples = re.split(pattern, local_test_input_data)
            for raw_example in examples:
                split = raw_example.split("-" * 80)
                input_data = split[0].strip("\n")
                parameters = split[1].strip("\n")
                parsed_parameters: dict[str, list[ProblemParameters]] = {"a": [], "b": []}

                wip: dict[str, Any] = {}
                extra: dict[str, str] = {}
                for line in parameters.split("\n"):
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split(": ", maxsplit=1)
                    if key == "extra":
                        k, v = value.split("=")
                        extra[k] = v
                        continue
                    part = key[-1:]
                    target = key[:-2]
                    if wip and (wip.get("part") != part or target in wip):
                        parsed_parameters[wip["part"]].append(
                            ProblemParameters(
                                kwargs=wip.get("kwargs", dict()),
                                answer=wip["answer"],
                            )
                        )
                        wip = {}
                    if value == "-":
                        continue
                    elif target == "kwargs":
                        value = json.loads(value)
                    wip["part"] = part
                    wip[target] = value
                if wip:
                    parsed_parameters[wip["part"]].append(
                        ProblemParameters(
                            kwargs=wip.get("kwargs", dict()),
                            answer=wip["answer"],
                        )
                    )
                if extra:
                    for parts in parsed_parameters:
                        for parameters in parsed_parameters[parts]:
                            for k, v in extra.items():
                                if k not in parameters.kwargs:
                                    parameters.kwargs[k] = v
                self.examples.append(
                    Prompt(
                        input_data=input_data,
                        part_one=parsed_parameters["a"],
                        part_two=parsed_parameters["b"],
                    )
                )
        except Exception as e:
            logger.info("Using API data for examples.")
            logger.trace(f"Failed to open/parse file. [{self.test_input_file}, {e=}]")
            for example in self.aoc_puzzle.examples:
                part_one = []
                part_two = []
                if example.answer_a:
                    part_one.append(ProblemParameters(answer=example.answer_a))
                if example.answer_b:
                    part_two.append(ProblemParameters(answer=example.answer_b))
                self.examples.append(
                    Prompt(
                        input_data=example.input_data,
                        part_one=part_one,
                        part_two=part_two,
                    )
                )
