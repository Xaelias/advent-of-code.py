from collections import defaultdict
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        crates_raw, moves_raw = input_data.as_chunks

        crates = defaultdict(list)
        for row in crates_raw[-2::-1]:
            for idx in range(1, len(row), 4):
                if row[idx] != " ":
                    crates[idx // 4 + 1].append(row[idx])

        moves = [
            tuple(map(int, (words[1], words[3], words[5])))
            for line in moves_raw
            if (words := line.split())
        ]
        return crates, moves

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> str:
        crates, moves = parsed_input
        for move in moves:
            qty, src, dst = move
            for _ in range(qty):
                popped = crates[src].pop()
                crates[dst].append(popped)
        return "".join(stack[-1] for i in range(10) if (stack := crates[i]))

    @classmethod
    def parse_part_two(cls, input_data: AoCInput) -> Any:
        # disable caching for dict
        return cls.cached_parse_part_one.__wrapped__(cls, input_data)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> str:
        crates, moves = parsed_input
        for move in moves:
            qty, src, dst = move
            popped, crates[src] = crates[src][-qty:], crates[src][:-qty]
            crates[dst].extend(popped)
        return "".join(stack[-1] for i in range(10) if (stack := crates[i]))
