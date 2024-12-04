from collections import namedtuple
from typing import Any
from typing import Self

from aocl.base import AoCInput
from aocl.base import Base

Draw = namedtuple("Draw", ["red", "green", "blue"])


class Game:
    def __init__(self, id: int) -> None:
        self.id = id
        self.draws: list[Draw] = []

    def __repr__(self) -> str:
        return f"<Game: {self.id} | {', '.join([f'r{draw.red} g{draw.green} b{draw.blue}' for draw in self.draws])}>"

    def draw(self, red: int = 0, green: int = 0, blue: int = 0) -> Self:
        draw = Draw(red=red, green=green, blue=blue)
        self.draws.append(draw)
        return self

    def is_possible(self, red: int = 0, green: int = 0, blue: int = 0) -> bool:
        for draw in self.draws:
            if draw.red > red or draw.green > green or draw.blue > blue:
                return False
        return True

    def __eq__(self, other):
        if self.id != other.id:
            return False
        if len(self.draws) != len(other.draws):
            return False
        for self_draw, other_draw in zip(self.draws, other.draws):
            if self_draw != other_draw:
                return False
        return True

    @staticmethod
    def parse_game(input: str) -> "Game":
        game_prefix, draws = input.split(": ")
        game_id = int(game_prefix[len("Game ") :])
        game = Game(game_id)
        for draw in draws.split("; "):
            red = 0
            green = 0
            blue = 0
            for color in draw.split(", "):
                if "red" in color:
                    red = int(color[: -len(" red")])
                if "green" in color:
                    green = int(color[: -len(" green")])
                if "blue" in color:
                    blue = int(color[: -len(" blue")])
            game.draw(red=red, green=green, blue=blue)
        return game

    def fewer_number_of_cubes(self) -> int:
        red = 0
        green = 0
        blue = 0
        for draw in self.draws:
            red = max(red, draw.red)
            green = max(green, draw.green)
            blue = max(blue, draw.blue)
        return red * green * blue


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return list(map(Game.parse_game, input_data.as_list_of_str))

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        return sum(game.id for game in parsed_input if game.is_possible(red=12, green=13, blue=14))

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        return sum(map(Game.fewer_number_of_cubes, parsed_input))
