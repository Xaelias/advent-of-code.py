from typing import Any

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[str]:
        return list(input_data.raw)

    @classmethod
    def move(cls, position: p2.P2, direction: str) -> p2.P2:
        match direction:
            case "^":
                position = p2.up(position)
            case ">":
                position = p2.right(position)
            case "<":
                position = p2.left(position)
            case _:
                position = p2.down(position)
        return position

    @classmethod
    def process_part_one(cls, parsed_input: list[str], **kwargs: Any) -> int:
        position = (0, 0)
        visited = {position}

        for direction in parsed_input:
            position = cls.move(position, direction)
            visited.add(position)
        return len(visited)

    @classmethod
    def process_part_two(cls, parsed_input: list[str], **kwargs: Any) -> int:
        santa = (0, 0)
        robot = (0, 0)
        visited = {santa}

        directions = parsed_input[::-1]

        while directions:
            santa_dir = directions.pop()
            robot_dir = directions.pop()
            santa = cls.move(santa, santa_dir)
            robot = cls.move(robot, robot_dir)
            visited.add(santa)
            visited.add(robot)
        return len(visited)
