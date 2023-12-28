import math
from contextlib import suppress
from dataclasses import dataclass
from typing import Any

from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base

# set_start_method("spawn")

with suppress(Exception):
    logger.level("FAILED", no=25, color="<red>")


@dataclass
class Link:
    src: str
    dst: str

    def __init__(self, src, dst):
        self.src = min(src, dst)
        self.dst = dst if self.src == src else src

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Link):
            return (
                self.src == other.src
                and self.dst == other.dst
                or self.src == other.dst
                and self.dst == other.src
            )
        return False

    def __hash__(self):
        return hash((self.src, self.dst))


def split_components(groups, uni_links, splitter, ignore):
    for idx, group in enumerate(groups):
        if splitter.src in group and splitter.dst in group:
            break
    else:
        return

    del groups[idx]

    new_groups = []
    for link in uni_links:
        src_group = None
        dst_group = None
        src_group_idx = None
        dst_group_idx = None
        for idx, group in enumerate(new_groups):
            if link.src in group:
                src_group = group
                src_group_idx = idx
            if link.dst in group:
                dst_group = group
                dst_group_idx = idx
            if src_group_idx is not None and dst_group_idx is not None:
                break
        if src_group_idx == dst_group_idx and dst_group_idx is not None:
            continue
        if link in ignore:
            if src_group_idx is None:
                new_groups.append({link.src})
            if dst_group_idx is None:
                new_groups.append({link.dst})
        else:
            if src_group_idx is None and dst_group_idx is None:
                new_groups.append({link.src, link.dst})
            elif src_group_idx is None:
                dst_group.add(link.src)
            elif dst_group_idx is None:
                src_group.add(link.dst)
            else:
                min_idx = min(src_group_idx, dst_group_idx)
                max_idx = max(src_group_idx, dst_group_idx) - 1
                del new_groups[min_idx]
                del new_groups[max_idx]
                new_groups.append(src_group.union(dst_group))
    groups.extend(new_groups)


def merge_components(groups, new_link):
    if len(groups) == 1:
        return
    src_group_idx = -1
    dst_group_idx = -1
    for idx, group in enumerate(groups):
        if new_link.src in group:
            src_group = group
            src_group_idx = idx
        if new_link.dst in group:
            dst_group = group
            dst_group_idx = idx
    if src_group_idx == dst_group_idx:
        return
    if src_group_idx == -1 or dst_group_idx == -1:
        return
    min_idx = min(src_group_idx, dst_group_idx)
    max_idx = max(src_group_idx, dst_group_idx) - 1
    del groups[min_idx]
    del groups[max_idx]
    groups.append(src_group.union(dst_group))  # noqa


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        verts = set()
        edges = set()
        for line in input_data.as_list_of_str:
            src, d = line.split(": ")
            destinations = d.split()
            verts.add(src)
            for dd in destinations:
                verts.add(dd)
                edges.add((src, dd))
        return verts, edges

    @classmethod
    def process_part_one(cls, parsed_input: Any, **kwargs: Any) -> int:
        from networkx import Graph
        from networkx import connected_components
        from networkx import minimum_edge_cut

        g = Graph()

        verts, edges = parsed_input
        for vertex in verts:
            g.add_node(vertex)
        for edge in edges:
            g.add_edge(*edge)

        load_bearing_edges = minimum_edge_cut(g)
        g.remove_edges_from(load_bearing_edges)
        return math.prod(map(len, connected_components(g)))

        # import igraph
        # g = igraph.Graph()
        # verts, edges = parsed_input
        # for vertex in verts:
        #     g.add_vertex(vertex)
        # for edge in edges:
        #     g.add_edge(*edge)
        # groups = g.mincut()
        # return math.prod(map(len, groups))

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> str:
        return ""
