from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


def remap_letters(letter: str) -> str:
    match letter:
        case "A" | "X":
            return "Rock"
        case "B" | "Y":
            return "Paper"
        case "C" | "Z":
            return "Scissors"
        case _:
            raise ValueError(f"Invalid letter {letter!r}")


def shape_point(shape: str) -> int:
    match shape:
        case "Rock":
            return 1
        case "Paper":
            return 2
        case "Scissors":
            return 3
        case _:
            raise ValueError(f"Invalid shape {shape!r}")


def win_draw_lose(theirs: str, mine: str) -> int:
    if theirs == mine:
        return 3
    if theirs == "Rock" and mine == "Paper":
        return 6
    if theirs == "Paper" and mine == "Scissors":
        return 6
    if theirs == "Scissors" and mine == "Rock":
        return 6
    return 0


def remap_letters_part_two(letter: str) -> str:
    match letter:
        case "A":
            return "Rock"
        case "B":
            return "Paper"
        case "C":
            return "Scissors"
        case "X":
            return "Lose"
        case "Y":
            return "Draw"
        case "Z":
            return "Win"
        case _:
            raise ValueError(f"Invalid letter {letter!r}")


def map_win_condition_to_shape(theirs: str, result: str) -> str:
    if result == "Draw":
        return theirs
    win = result == "Win"
    match theirs:
        case "Rock":
            return "Paper" if win else "Scissors"
        case "Paper":
            return "Scissors" if win else "Rock"
        case "Scissors":
            return "Rock" if win else "Paper"
        case _:
            raise ValueError(f"Invalid shape {theirs!r}")


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        rounds = []
        for row in input_data.as_list_of_str:
            rounds.append(tuple(map(remap_letters, row.split())))
        return rounds

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        total = 0
        for round in parsed_input:
            opponent, me = round
            total += win_draw_lose(opponent, me) + shape_point(me)
        return total

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        rounds = []
        for row in input_data.as_list_of_str:
            rounds.append(tuple(map(remap_letters_part_two, row.split())))
        return rounds

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        new_rounds = []
        for round in parsed_input:
            theirs, result = round
            new_rounds.append((theirs, map_win_condition_to_shape(theirs, result)))
        return cls.process_part_one(new_rounds)
