import os
from collections import defaultdict
from typing import Any

from aocl.base import AoCInput
from aocl.base import Base


def recursive_dir_size(file_sizes: dict[str, int], subdirs: dict[str, list[str]], dir: str) -> int:
    return file_sizes[dir] + sum(
        recursive_dir_size(file_sizes, subdirs, os.path.join(dir, sub)) for sub in subdirs[dir]
    )


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        file_sizes: dict[str, int] = defaultdict(int)
        subdirs = defaultdict(list)
        current_dir = "/"
        for line in input_data.as_list_of_str:
            if line.startswith("$ cd"):
                dst = line.split()[2]
                if dst == "/":
                    current_dir = "/"
                elif dst == "..":
                    current_dir = current_dir.rsplit("/", maxsplit=1)[0] or "/"
                else:
                    current_dir = os.path.join(current_dir, dst)
            elif line.startswith("$ ls"):
                continue
            elif line.startswith("dir "):
                _, subdir = line.split()
                subdirs[current_dir].append(subdir)
                file_sizes[os.path.join(current_dir, subdir)]  # noqa
            else:
                size, _ = line.split()
                file_sizes[current_dir] += int(size)
        return {
            k: recursive_dir_size(file_sizes, subdirs, k)
            for k in set(file_sizes.keys()) | set(subdirs.keys())
        }

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        dir_sizes = parsed_input
        return sum(v for v in dir_sizes.values() if v <= 100_000)

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int:
        dir_sizes = parsed_input
        space_needed = 30000000 - (70000000 - dir_sizes["/"])
        return min(v for v in dir_sizes.values() if v >= space_needed)
