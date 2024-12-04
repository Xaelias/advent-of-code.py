import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import Any
from typing import Iterable
from typing import Self

from aocl.base import AoCInput
from aocl.base import Base


@dataclass
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int
    # name: str

    def __init__(self, a: int, b: int, c: int, x: int, y: int, z: int, name="") -> None:
        self.x1 = [a, x][z < c]
        self.y1 = [b, y][z < c]
        self.z1 = [c, z][z < c]
        self.x2 = [a, x][z >= c]
        self.y2 = [b, y][z >= c]
        self.z2 = [c, z][z >= c]
        self.name = name

        assert self.z1 <= self.z2

    def __hash__(self) -> int:
        return hash((self.x1, self.y1, self.z1, self.x2, self.y2, self.z2))

    def __repr__(self) -> str:
        return f"{self.name} ({self.x1} {self.y1} {self.z1}, {self.x2} {self.y2} {self.z2})"

    @staticmethod
    @cache
    def touches(x1: int, y1: int, x2: int, y2: int, xx1: int, yy1: int, xx2: int, yy2: int) -> bool:
        x_seg = (min(x1, x2), max(x1, x2))
        y_seg = (min(y1, y2), max(y1, y2))

        xx_seg = (min(xx1, xx2), max(xx1, xx2))
        yy_seg = (min(yy1, yy2), max(yy1, yy2))

        return (
            x_seg[0] <= xx_seg[1]
            and xx_seg[0] <= x_seg[1]
            and y_seg[0] <= yy_seg[1]
            and yy_seg[0] <= y_seg[1]
        )

    def is_supported_by(self, other: Self) -> bool:
        return (self.z1 == other.z2 + 1) and self.touches(
            other.x1,
            other.y1,
            other.x2,
            other.y2,
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        )

    def go_down(self, levels: int = 1) -> Self:
        return type(self)(
            self.x1, self.y1, self.z1 - levels, self.x2, self.y2, self.z2 - levels, self.name
        )


class Snapshot:
    floor = Brick(0, 0, 0, 0, 0, 0, "_")

    def __init__(self, bricks: Iterable[Brick]):
        self.lower_elevation: dict[int, set[Brick]] = defaultdict(set)
        self.higher_elevation: dict[int, set[Brick]] = defaultdict(set)
        self.is_supported_by: dict[Brick, set[Brick]] = defaultdict(set)

        for brick in bricks:
            self._add_brick(brick)

        while to_process := self._can_go_down():
            for brick in to_process:
                new_brick = brick.go_down()
                self._rem_brick(brick)
                self._add_brick(new_brick)

    @property
    def size(self) -> int:
        return len(self.is_supported_by)

    def _can_go_down(self) -> set[Brick]:
        return {brick for brick, supports in self.is_supported_by.items() if not supports}

    def _add_brick(self, brick: Brick) -> None:
        self.lower_elevation[brick.z1].add(brick)
        self.higher_elevation[brick.z2].add(brick)
        self.is_supported_by[brick]  # noqa

        for other in self.lower_elevation[brick.z2 + 1]:
            if other.is_supported_by(brick):
                self.is_supported_by[other].add(brick)
        if brick.z1 == 1:
            self.is_supported_by[brick].add(self.floor)
        else:
            for other in self.higher_elevation[brick.z1 - 1]:
                if brick.is_supported_by(other):
                    self.is_supported_by[brick].add(other)

    def _rem_brick(self, brick: Brick) -> None:
        self.lower_elevation[brick.z1].remove(brick)
        self.higher_elevation[brick.z2].remove(brick)

        self.is_supported_by.pop(brick)
        for other in self.lower_elevation[brick.z2 + 1]:
            self.is_supported_by[other].discard(brick)


class Solution(Base):
    @classmethod
    def next_brick_name(cls, name: str, new_name: str = "") -> str:
        if not name:
            return "A" + new_name
        head, tail = name[:-1], name[-1]
        if tail == "Z":
            return cls.next_brick_name(head, "A" + new_name)
        return head + chr(65 + (ord(tail) - 65 + 1) % 26) + new_name

    @classmethod
    @cache
    def parse(cls, input: AoCInput) -> Any:
        bricks = []
        name = "A"

        for line in input.as_list_of_str:
            a, b, c, x, y, z = [int(s) for s in re.findall(r"[0-9]+", line)]
            bricks.append(Brick(a, b, c, x, y, z, name))
            name = cls.next_brick_name(name)

        return Snapshot(bricks)

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        snapshot = parsed_input

        spof = {
            next(iter(supports))
            for _, supports in snapshot.is_supported_by.items()
            if len(supports) == 1
        }
        spof.discard(snapshot.floor)

        return snapshot.size - len(spof)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        snapshot = parsed_input

        spof = {next(iter(v)) for k, v in snapshot.is_supported_by.items() if len(v) == 1}
        spof.discard(snapshot.floor)

        total = 0
        for brick in spof:
            destroying = defaultdict(set, {brick.z2: {brick}})
            change = True
            while change:
                change = False
                for candidate, needed in snapshot.is_supported_by.items():
                    if candidate.z2 in destroying and candidate in destroying[candidate.z2]:
                        continue
                    if (candidate.z1 - 1) in destroying and needed.issubset(
                        destroying[candidate.z1 - 1]
                    ):
                        destroying[candidate.z2].add(candidate)
                        change = True

            count = len(set.union(*destroying.values())) - 1
            total += count
        return total
