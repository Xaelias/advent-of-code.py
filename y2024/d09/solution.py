import bisect
from dataclasses import dataclass
from operator import attrgetter
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base
from aocl.base import logger


@dataclass
class Node:
    file_id: int
    position: int
    size: int

    def checksum(self) -> int:
        return sum(range(self.position, self.position + self.size)) * self.file_id

    def __repr__(self) -> str:
        return f"<File {self.file_id}: {self.position} #{self.size}>"


class Disk:
    def __init__(self, disk_map: list[int]):
        self.nodes: list[Node] = []
        self.frees: list[Node] = []

        pos = 0
        for idx in range(len(disk_map)):
            size = disk_map[idx]
            if idx % 2 == 0:
                self.nodes.append(
                    Node(
                        file_id=idx // 2,
                        position=pos,
                        size=size,
                    )
                )
            else:
                self.frees.append(
                    Node(
                        file_id=-1,
                        position=pos,
                        size=size,
                    )
                )
            pos += size

    def move_bytes(self, inode: int, ifree: int, count: int | None = None):
        node = self.nodes[inode]
        if count is None:
            count = node.size
        free = self.frees[ifree]

        logger.trace(f"Move {count} bytes from {node} to {free}")

        if count == node.size:
            node.position = free.position
            del self.nodes[inode]
            bisect.insort_left(self.nodes, node, key=attrgetter("position"))
        else:
            new_node = Node(file_id=node.file_id, position=free.position, size=count)
            bisect.insort_left(self.nodes, new_node, key=attrgetter("position"))
            node.size -= count

        free.size -= count
        free.position += count
        if free.size == 0:
            del self.frees[ifree]

    def checksum(self):
        return sum((node.checksum() for node in self.nodes))

    def has_free_space(self, inode: int) -> int | None:
        node = self.nodes[inode]
        for idx, free in enumerate(self.frees):
            if free.position >= node.position:
                return None
            if free.size >= node.size:
                return idx
        return None

    def __repr__(self) -> str:
        pos = 0
        result = ""
        for node in self.nodes:
            result += "." * (node.position - pos)
            result += str(node.file_id)[-1] * node.size
            pos = node.position + node.size
        return result


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> list[int]:
        return list(map(int, iter(input_data.raw)))

    @classmethod
    def process_part_one(cls, parsed_input: list[int], **kwargs: Any) -> int:
        disk = Disk(parsed_input)
        logger.debug(disk)
        while len(disk.frees) > 0 and disk.nodes[-1].position > disk.frees[0].position:
            disk.move_bytes(
                inode=len(disk.nodes) - 1,
                ifree=0,
                count=min(disk.frees[0].size, disk.nodes[-1].size),
            )
            logger.trace(disk)
        logger.debug(disk)

        return disk.checksum()

    @classmethod
    def process_part_two(cls, parsed_input: list[int], **kwargs: Any) -> int:
        disk = Disk(parsed_input)
        logger.debug(disk)
        inode = len(disk.nodes) - 1
        while len(disk.frees) > 0 and disk.nodes[inode].position > disk.frees[0].position:
            if (ifree := disk.has_free_space(inode)) is not None:
                disk.move_bytes(inode, ifree)
                logger.trace(disk)
            else:
                inode -= 1

        logger.debug(disk)
        return disk.checksum()
