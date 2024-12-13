import hashlib
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> str:
        return input_data.raw

    @classmethod
    def process_part_one(cls, parsed_input: str, leading_zeros: int = 5, **kwargs: Any) -> int:
        return next(
            (
                i
                for i in range(1000000000)
                if hashlib.md5(f"{parsed_input}{i}".encode())
                .hexdigest()
                .startswith("0" * leading_zeros)
            )
        )

    @classmethod
    def process_part_two(cls, parsed_input: str, **kwargs: Any) -> int:
        return cls.process_part_one(parsed_input, leading_zeros=6)
