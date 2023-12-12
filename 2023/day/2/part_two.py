#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur <Me@ALesieur.net>
# Date              : 2023/12/02 10:39:49
# Last Modified Date: 2023/12/02 10:50:38
# Last Modified By  : Alexis Lesieur <Me@ALesieur.net>
import os
import sys

from loguru import logger
from part_one import Game, Draw
from part_one import g1, g2, g3, g4, g5, games


def fewer_number_of_cubes(game: Game) -> int:
    red = 0
    green = 0
    blue = 0
    for draw in game.draws:
        red = max(red, draw.red)
        green = max(green, draw.green)
        blue = max(blue, draw.blue)
    draw = Draw(red=red, green=green, blue=blue)
    logger.info(f"Game {game.id} was possible with {draw=}")
    return red * green * blue


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./input")
    total = 0
    with open(input, "r") as f:
        for line in f.readlines():
            game = Game.parse_game(line.strip())
            total += fewer_number_of_cubes(game)
    logger.info(f"Total is {total}.")


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)



def test_provided(games):
    assert fewer_number_of_cubes(games[1]) == 48
    assert fewer_number_of_cubes(games[2]) == 12
    assert fewer_number_of_cubes(games[3]) == 1560
    assert fewer_number_of_cubes(games[4]) == 630
    assert fewer_number_of_cubes(games[5]) == 36
