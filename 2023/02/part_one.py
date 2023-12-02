#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur <Me@ALesieur.net>
# Date              : 2023/12/02 09:29:49
# Last Modified Date: 2023/12/02 10:50:18
# Last Modified By  : Alexis Lesieur <Me@ALesieur.net>
from collections import namedtuple
from loguru import logger

import os
import pytest
import sys


class Draw:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue


Draw = namedtuple("Draw", ["red", "green", "blue"])

class Game:
    def __init__(self, id: int):
        self.id = id
        self.draws = []

    def __repr__(self):
        return f"<Game: {self.id} | {', '.join([f'r{draw.red} g{draw.green} b{draw.blue}' for draw in self.draws])}>"

    def draw(self, red: int = 0, green: int = 0, blue: int = 0):
        draw = Draw(red=red, green=green, blue=blue)
        self.draws.append(draw)
        logger.debug(f"Added draw. [{self=}, {draw=}]")
        return self

    def is_possible(self, red: int=0, green: int=0, blue: int=0):
        for draw in self.draws:
            logger.debug(f"Testing solution against draw. [{draw=}, {red=}, {green=}, {blue=}]")
            if draw.red > red or draw.green > green or draw.blue > blue:
                logger.info(f"Game {self.id} is not possible. [{draw=}, {red=}, {green=}, {blue=}]")
                return False
        logger.info(f"Game {self.id} is possible with {red:2d} red, {green:2d} green, {blue:2d} cubes.")
        return True

    def __eq__(self, other):
        if self.id != other.id:
            logger.debug(f"{self=} and {other=} have different ids")
            return False
        if self.red != other.red:
            return False
        if self.green != other.green:
            return False
        if self.blue != other.blue:
            return False
        if len(self.draws) != len(other.draws):
            return False
        for self_draw, other_draw in zip(self.draws, other.draws):
            if self_draw != other_draw:
                return False
        return True

    @staticmethod
    def parse_game(input:str) -> "Game":
        game_id, draws = input.split(": ")
        game_id = int(game_id[len("Game "):])
        game = Game(game_id)
        for draw in draws.split("; "):
            red = 0
            green = 0
            blue = 0
            for color in draw.split(", "):
                if "red" in color:
                    red = int(color[:-len(" red")])
                if "green" in color:
                    green = int(color[:-len(" green")])
                if "blue" in color:
                    blue = int(color[:-len(" blue")])
            game.draw(red=red, green=green, blue=blue)
        return game


@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./input")
    possible_games = []
    with open(input, "r") as f:
        for line in f.readlines():
            game = Game.parse_game(line.strip())
            if game.is_possible(red=12, green=13, blue=14):
                possible_games.append(game)
    possible_ids = [g.id for g in possible_games]
    logger.info(f"The following games are possible: {possible_ids}. Total = {sum(possible_ids)}.")


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)


@pytest.fixture()
def g1():
    yield Game(1).draw(blue=3, red=4).draw(red=1, green=2, blue=6).draw(green=2)
@pytest.fixture()
def g2():
    yield Game(2).draw(blue=1, green=2).draw(green=3, blue=4, red=1).draw(green=1, blue=1)
@pytest.fixture()
def g3():
    yield Game(3).draw(green=8, blue=6, red=20).draw(blue=5, red=4, green=13).draw(green=5, red=1)
@pytest.fixture()
def g4():
    yield Game(4).draw(green=1, red=3, blue=6).draw(green=3, red=6).draw(green=3, blue=15, red=14)
@pytest.fixture()
def g5():
    yield Game(5).draw(red=6, blue=1, green=3).draw(blue=2, red=1, green=2)

@pytest.fixture()
def games(g1, g2, g3, g4, g5):
    yield {
        1: g1,
        2: g2,
        3: g3,
        4: g4,
        5: g5,
    }


def test_is_possible(games):
    assert games[1].is_possible(red=12, green=13, blue=14)
    assert games[2].is_possible(red=12, green=13, blue=14)
    assert not games[3].is_possible(red=12, green=13, blue=14)
    assert not games[4].is_possible(red=12, green=13, blue=14)
    assert games[5].is_possible(red=12, green=13, blue=14)

def test_is_possible_edge_case():
    g = Game(1).draw(red=20).draw(red=20).draw(red=2)
    assert g.is_possible(red=20)
    assert not g.is_possible(red=3)

def test_equal(games):
    assert games[1] == games[1]
    assert games[2] == games[2]
    assert games[3] == games[3]
    assert games[4] == games[4]
    assert games[5] == games[5]
    assert games[1] != games[2]
    assert games[1] != games[3]
    assert games[1] != games[4]
    assert games[1] != games[5]

def test_parse(games):
    assert parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == games[1]
    assert parse_game("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue") == games[2]
    assert parse_game("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red") == games[3]
    assert parse_game("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red") == games[4]
    assert parse_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green") == games[5]
