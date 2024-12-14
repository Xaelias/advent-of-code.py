import operator
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[tuple[Any, ...]]:
        def cast_int(tbd: str | None) -> str | int | None:
            try:
                return int(tbd)  # type: ignore
            except Exception:
                return tbd

        instructions = []
        for line in input_data.as_lines:
            left: str | None = None
            op = None
            right: str | None = None
            instruction, var = line.split(" -> ")
            if "AND" in instruction:
                left, _, right = instruction.partition(" AND ")
                op = operator.and_
            elif "OR" in instruction:
                left, _, right = instruction.partition(" OR ")
                op = operator.or_
            elif "LSHIFT" in instruction:
                left, _, right = instruction.partition(" LSHIFT ")
                op = operator.lshift
            elif "RSHIFT" in instruction:
                left, _, right = instruction.partition(" RSHIFT ")
                op = operator.rshift
            elif "NOT" in instruction:
                left = instruction[4:]
                op = operator.xor
                right = "0xFFFF"
            else:
                right = instruction

            instructions.append((cast_int(left), op, cast_int(right), var))
        return instructions

    @classmethod
    def process_part_one(cls, parsed_input: list[tuple[Any, ...]], **kwargs: Any) -> int:
        variables: dict[str, int] = {}
        for instruction in parsed_input:
            left_v, op, right_v, var = instruction

            try:
                left = None
                if isinstance(left_v, int):
                    left = left_v
                elif left_v is not None:
                    left = variables[left_v]

                right = None
                if isinstance(right_v, int):
                    right = right_v
                elif right_v is not None:
                    right = variables[right_v]
            except KeyError:
                # we haven't calculated this variable yet, will come back
                parsed_input.append(instruction)
                continue

            if op is None:
                variables[var] = right  # type: ignore
            else:
                variables[var] = op(right) if left is None else op(left, right)
        return variables[kwargs.get("wire", "a")]

    @classmethod
    def process_part_two(cls, parsed_input: list[tuple[Any, ...]], **kwargs: Any) -> int:
        new_b = cls.process_part_one(parsed_input, **kwargs)

        instructions = []
        for instruction in parsed_input:
            left_v, op, right_v, var = instruction

            if op is None and var == "b":
                right_v = new_b

            instructions.append((left_v, op, right_v, var))

        # could probably also cache a lot of the results from part one :shrug:
        return cls.process_part_one(instructions, **kwargs)
