import itertools
from typing import Any

from aocl import p2
from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import logger

type Antinode = p2.P2
type Antenna = p2.P2


def draw_map(matrix: p2.StrMatrix, antinodes: set[p2.P2]) -> str:
    shape = p2.shape(matrix)

    result = [""]

    for i in range(shape[0]):
        row = []
        for j in range(shape[1]):
            og = matrix[i][j]
            if (i, j) in antinodes and og == ".":
                row.append("#")
            else:
                row.append(og)
        result.append("".join(row))
    return "\n".join(result)


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> p2.StrMatrix:
        return input_data.as_list_of_lists

    @classmethod
    def process_part_one(cls, parsed_input: p2.StrMatrix, **kwargs: Any) -> int:
        antinodes: set[Antinode] = set()
        shape = p2.shape(parsed_input)
        # not the most efficient :shrug:
        frequencies = p2.matrix_unique(parsed_input)
        for frequency in frequencies:
            if frequency == ".":
                continue
            logger.debug(f"processing all antennas w/ frequency {frequency}")

            antennas: list[Antenna] = p2.where_in_matrix(parsed_input, frequency)
            logger.trace(f"found {len(antennas)} antennas w/ frequency {frequency}")

            for antenna_a, antenna_b in itertools.combinations(antennas, 2):
                logger.trace(f"processing pair {antenna_a} - {antenna_b}")
                delta = p2.sub(antenna_b, antenna_a)
                antinode_a = p2.sub(antenna_a, delta)
                antinode_b = p2.add(antenna_b, delta)

                if p2.in_shape(antinode_a, shape):
                    logger.debug(f"adding antinode {antinode_a} for {antenna_a}-{antenna_b}")
                    antinodes.add(antinode_a)

                if p2.in_shape(antinode_b, shape):
                    logger.debug(f"adding antinode {antinode_b} for {antenna_a}-{antenna_b}")
                    antinodes.add(antinode_b)

        logger.trace(draw_map(parsed_input, antinodes))
        return len(antinodes)

    @classmethod
    def process_part_two(cls, parsed_input: p2.StrMatrix, **kwargs: Any) -> int:
        antinodes: set[Antinode] = set()
        shape = p2.shape(parsed_input)
        # not the most efficient :shrug:
        frequencies = p2.matrix_unique(parsed_input)
        for frequency in frequencies:
            if frequency == ".":
                continue
            logger.debug(f"processing all antennas w/ frequency {frequency}")

            antennas: list[Antenna] = p2.where_in_matrix(parsed_input, frequency)
            logger.trace(f"found {len(antennas)} antennas w/ frequency {frequency}")

            for antenna_a, antenna_b in itertools.combinations(antennas, 2):
                logger.trace(f"processing pair {antenna_a} - {antenna_b}")
                delta = p2.sub(antenna_b, antenna_a)

                candidate = antenna_a
                while p2.in_shape(candidate, shape):
                    antinodes.add(candidate)
                    candidate = p2.sub(candidate, delta)

                candidate = antenna_b
                while p2.in_shape(candidate, shape):
                    antinodes.add(candidate)
                    candidate = p2.add(candidate, delta)

        logger.trace(draw_map(parsed_input, antinodes))
        return len(antinodes)
