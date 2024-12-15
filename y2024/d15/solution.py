from collections.abc import Callable
from typing import Any

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import logger


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> tuple[p2.StrMatrix, list[Callable]]:
        mapping = {"^": p2.up, "<": p2.left, ">": p2.right, "v": p2.down}

        matrix, movements = input_data.as_chunks
        warehouse = [list(line) for line in matrix]
        directions = [mapping[c] for line in movements for c in line]
        return warehouse, directions

    @classmethod
    def print_warehouse(cls, warehouse: p2.StrMatrix, robot: p2.P2) -> str:
        drawing = [""]
        height, width = p2.shape(warehouse)
        for i in range(height):
            row = []
            for j in range(width):
                if (i, j) == robot:
                    row.append("@")
                else:
                    row.append(p2.matrix_get(warehouse, (i, j)))
            drawing.append("".join(row))
        return "\n".join(drawing)

    @classmethod
    def score_warehouse(cls, warehouse: p2.StrMatrix) -> int:
        height, width = p2.shape(warehouse)
        score = 0
        for i in range(height):
            for j in range(width):
                if p2.matrix_get(warehouse, (i, j)) in "O[":
                    score += 100 * i + j
        return score

    @classmethod
    def process_part_one(
        cls,
        parsed_input: tuple[p2.StrMatrix, list[Callable]],
        **kwargs: Any,
    ) -> int:
        warehouse, directions = parsed_input
        # need to copy because caching :awkward:
        warehouse = [[c for c in line] for line in warehouse]

        robot = p2.where_in_matrix(warehouse, "@")[0]
        p2.matrix_set(warehouse, robot, ".")

        logger.trace("{x}", x=lambda: cls.print_warehouse(warehouse, robot))

        for direction in directions:
            new_position = direction(robot)
            match p2.matrix_get(warehouse, new_position):
                case "#":
                    logger.info(
                        f"<red>✘</red> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                    )
                    pass
                case ".":
                    logger.info(
                        f"<green>✔</green> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                    )
                    robot = new_position
                case "O":
                    box = new_position
                    count = 1
                    while p2.matrix_get(warehouse, (box := direction(box))) == "O":
                        count += 1
                    if p2.matrix_get(warehouse, box) == ".":
                        logger.info(
                            f"<green>✔</green> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                        )
                        logger.debug(f"  <green>✔</green> move {count} boxes {direction.__name__}")
                        robot = new_position
                        p2.matrix_set(warehouse, box, "O")
                        p2.matrix_set(warehouse, robot, ".")
                    else:
                        logger.info(
                            f"<red>✘</red> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                        )
                        logger.debug(f"  <red>✘</red> move {count} boxes {direction.__name__}")
            logger.trace("{x}", x=lambda: cls.print_warehouse(warehouse, robot))

        return cls.score_warehouse(warehouse)

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> tuple[p2.StrMatrix, list[Callable]]:
        old_warehouse, directions = cls.parse(input_data)
        warehouse = []
        for old_line in old_warehouse:
            line = []
            for char in old_line:
                match char:
                    case "#":
                        line.append("#")
                        line.append("#")
                    case ".":
                        line.append(".")
                        line.append(".")
                    case "O":
                        line.append("[")
                        line.append("]")
                    case "@":
                        line.append("@")
                        line.append(".")
            warehouse.append(line)
        return warehouse, directions

    @classmethod
    def process_part_two(
        cls,
        parsed_input: tuple[p2.StrMatrix, list[Callable]],
        **kwargs: Any,
    ) -> int:
        warehouse, directions = parsed_input
        # need to copy because caching :awkward:
        warehouse = [[c for c in line] for line in warehouse]

        robot = p2.where_in_matrix(warehouse, "@")[0]
        p2.matrix_set(warehouse, robot, ".")

        logger.trace("{x}", x=lambda: cls.print_warehouse(warehouse, robot))

        def can_move_box(warehouse: p2.StrMatrix, pos: p2.P2, direction: Callable) -> bool:
            if p2.matrix_get(warehouse, pos) == ".":
                return True
            if p2.matrix_get(warehouse, pos) == "#":
                return False

            if direction in (p2.left, p2.right):
                while (val := p2.matrix_get(warehouse, (pos := direction(pos)))) in "[]":
                    pass
                return val == "."

            positions = (
                pos,
                p2.right(pos) if p2.matrix_get(warehouse, pos) == "[" else p2.left(pos),
            )

            return all(can_move_box(warehouse, direction(p), direction) for p in positions)

        def actually_move_box(warehouse: p2.StrMatrix, pos: p2.P2, direction: Callable) -> int:
            if p2.matrix_get(warehouse, pos) == ".":
                return 0

            count = 1
            if direction in (p2.left, p2.right):
                count += 1
                p2.matrix_set(warehouse, pos, ".")
                while (val := p2.matrix_get(warehouse, (pos := direction(pos)))) in "[]":
                    p2.matrix_set(warehouse, pos, "]" if val == "[" else "[")
                p2.matrix_set(warehouse, pos, "]" if direction == p2.right else "[")
                return count // 2

            positions = (
                pos,
                p2.right(pos) if p2.matrix_get(warehouse, pos) == "[" else p2.left(pos),
            )
            count = 1
            count += actually_move_box(warehouse, direction(positions[0]), direction)
            count += actually_move_box(warehouse, direction(positions[1]), direction)
            for pos in positions:
                p2.matrix_set(warehouse, direction(pos), p2.matrix_get(warehouse, pos))
                p2.matrix_set(warehouse, pos, ".")

            return count

        for direction in directions:
            new_position = direction(robot)
            match p2.matrix_get(warehouse, new_position):
                case "#":
                    logger.info(
                        f"<red>✘</red> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                    )
                    pass
                case ".":
                    logger.info(
                        f"<green>✔</green> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                    )
                    robot = new_position
                case "[" | "]":
                    box = new_position
                    if can_move_box(warehouse, box, direction):
                        count = actually_move_box(warehouse, box, direction)
                        logger.info(
                            f"<green>✔</green> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                        )
                        logger.debug(f"  <green>✔</green> moved {count} boxes {direction.__name__}")
                        robot = new_position
                    else:
                        logger.info(
                            f"<red>✘</red> move from {robot} --{direction.__name__:-^5}-> {new_position}"
                        )
                        logger.debug(f"  <red>✘</red> cannot move box(es) {direction.__name__}")
            logger.trace("{x}", x=lambda: cls.print_warehouse(warehouse, robot))

        return cls.score_warehouse(warehouse)
