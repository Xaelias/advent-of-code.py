import os
from abc import ABC
from abc import abstractmethod
from collections.abc import Iterator
from contextlib import suppress
from typing import Any
from typing import Optional

from functional import seq
from functional.pipeline import Sequence
from loguru import logger

with suppress(Exception):
    logger.level("FAILED", no=41, color="<red>")


class Input:
    def __init__(self, file_name: str):
        if os.path.exists(file_name):
            self.file_path = file_name
        elif os.path.exists(file_path := os.path.join(os.path.dirname(__file__), file_name)):
            self.file_path = file_path
        assert hasattr(self, "file_path")

        self.file_name = os.path.basename(self.file_path)

    @property
    def as_str(self) -> list[str]:
        with open(self.file_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    @property
    def as_iter(self) -> Iterator[str]:
        return iter(self.as_str)

    @property
    def as_seq(self) -> Sequence:
        return seq(self.as_str)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.file_name}>"

    def __iter__(self) -> Iterator[str]:
        return self.as_iter


class Prompt:
    def __init__(self, input: Input, expected: Optional[int], **kwargs: Any):
        self.input = input
        self.expected = expected
        self.kwargs = kwargs


class PartZero(ABC):
    parsed: dict[Input, Any] = {}

    @staticmethod
    @abstractmethod
    def process(parsed_input: Any, **kwargs: Any) -> int:
        ...

    @classmethod
    @abstractmethod
    def parse(cls, input: Input) -> Any:
        ...

    @classmethod
    def solve(cls, prompt: Prompt) -> bool:
        solution = cls.process(cls.parse(prompt.input), **prompt.kwargs)
        expected = prompt.expected
        if expected is None:
            logger.warning(f"{cls!r} Found {solution:,d} ({solution}). No expected value provided.")
        elif expected == solution:
            logger.success(f"{cls!r} Found {solution:,d} ({solution}).")
        else:
            logger.log("FAILED", f"{cls!r} Found {solution:,d} != expected {expected:,d}.")
        return expected is not None and solution == expected
