#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur
# Date              : 2023/12/05 18:06:18
# Last Modified Date: 2023/12/05 22:48:46
# Last Modified By  : Alexis Lesieur
import os
import pytest
import re
import sys

from collections import OrderedDict
from loguru import logger
from typing import Optional


# https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def extract_numbers(line: str) -> list[int]:
    logger.trace(f"Extracing numbers from line: {line}")
    matches = re.findall(r"\d+", line)
    logger.trace(f"Extracted numbers from line. [{line=}, {matches=}]")
    return [int(match) for match in matches]

class Range:
    def __init__(self, start: int, size: int):
        self.start = start
        self.size = size
        self.end = start + size - 1

    def __eq__(self, other) -> bool:
        return self.start == other.start and self.end == other.end
    def __lt__(self, other) -> bool:
        return self.start < other.start
    def __gt__(self, other) -> bool:
        return self.start > other.start

    def __repr__(self) -> bool:
        return f"<{self.__class__.__name__}: {self.start} - {self.end}>"
    def __contains__(self, other) -> bool:
        logger.trace(f"Testing if {other=} in {self=}.")
        if isinstance(other, int):
            return self.start <= other <= self.end
        if isinstance(other, self.__class__):
            return self.start <= other.start and other.end <= self.end

    def touches(self, other: "Range") -> list["Range"]:
        return self.start in other or self.end in other or other.start in self or other.end in self

    def split_range(self, other: "Range") -> list["Range"]:
        logger.trace(f"Testing if {other=} intersect with {self=}")
        if other.size == 1:
            logger.trace(f"Input is of size one, nothing to do")
            return [other]
        if not self.touches(other):
            logger.trace(f"Skiping computing intersection of distinct ranges.")
            return [other]

        limits = [e for e in sorted(list({self.start, self.end, other.start, other.end})) if other.start <= e <= other.end]
        logger.trace(f"Found limits. [{self=}, {other=}, {limits=}]")
        ranges = []
        prev = limits[0]
        for next in limits[1:]:
            if prev not in self and next not in self:
                # exclusively after self
                new_range = Range(prev, next - prev + 1)
                prev = next
            elif prev not in self:
                # before self
                new_range = Range(prev, next - prev)
                logger.trace(f"Computing range where prev not in self. [{self=}, {prev=}, {next=}, {new_range=}]")
                prev = next
            else:
                # in self
                new_range = Range(prev, next - prev + 1)
                logger.trace(f"Computing range where prev in self. [{self=}, {prev=}, {next=}, {new_range=}]")
                prev = next + 1
            ranges.append(new_range)

        return ranges


class Seed:
    def __init__(self, id: int):
        self.id = id

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"

    def __eq__(self, other):
        return self.id == other.id

class SeedRange(Range):
    pass

class AlmanacMap:
    def __init__(self, dst_start: int, src_start: int, size: int):
        self.src = Range(src_start, size)
        self.dst = Range(dst_start, size)
        self.size = size

    def __repr__(self):
        return f"<{self.__class__.__name__}: src={self.src}, dst={self.dst}, size={self.size}>"

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst and self.size == other.size

    def map_int_from_src_to_dst(self, src: int) -> Optional[int]:
        logger.trace(f"{self=} - trying to find mapping for {src}")
        if src in self.src:
            return (src - self.src.start) + self.dst.start
        return None

    def map_range(self, r: Range) -> tuple[list[Range], list[Range]]:
        logger.trace(f"Mapping a single range. [{self=}, {r=}]")
        mapped = []
        untouched = []
        for r in self.src.split_range(r):
            logger.trace(f"Processing one intersection. [{self=}, {r=}]")
            if r in self.src:
                mapped.append(Range(self.dst.start + (r.start - self.src.start), r.size))
                logger.trace(f"New mapped range. [{self=}, {mapped[-1]=}]")
            else:
                untouched.append(r)
                logger.trace(f"New untouched range. [{self=}, {untouched[-1]=}]")
        return mapped, untouched

    def map_ranges(self, ranges: list[Range]) -> tuple[list[Range], list[Range]]:
        mapped = []
        untouched = []

        for r in ranges:
            new_mapped, new_untouched = self.map_range(r)
            mapped.extend(new_mapped)
            untouched.extend(new_untouched)

        return mapped, untouched



class Seed2Soil(AlmanacMap):
    pass
class Soil2Fertilizer(AlmanacMap):
    pass
class Fertilizer2Water(AlmanacMap):
    pass
class Water2Light(AlmanacMap):
    pass
class Light2Temperature(AlmanacMap):
    pass
class Temperature2Humidity(AlmanacMap):
    pass
class Humidity2Location(AlmanacMap):
    pass

class Almanac:
    def __init__(
        self,
        seeds: list[Seed],
        seed_to_soil: list[Seed2Soil],
        soil_to_fertilizer: list[Soil2Fertilizer],
        fertilizer_to_water: list[Fertilizer2Water],
        water_to_light: list[Water2Light],
        light_to_temperature: list[Light2Temperature],
        temperature_to_humidity: list[Temperature2Humidity],
        humidity_to_location: list[Humidity2Location],
    ):
        self.seeds = seeds
        self.maps = OrderedDict([
            ("seed_to_soil", seed_to_soil),
            ("soil_to_fertilizer", soil_to_fertilizer),
            ("fertilizer_to_water", fertilizer_to_water),
            ("water_to_light", water_to_light),
            ("light_to_temperature", light_to_temperature),
            ("temperature_to_humidity", temperature_to_humidity),
            ("humidity_to_location", humidity_to_location),
        ])

    @classmethod
    def parse_input(cls, iterable) -> "self":
        logger.trace(f"Extracting seeds.")
        line = next(iterable)
        seeds = [Seed(int(i)) for i in re.findall(r"\d+", line)]
        logger.debug(f"Extraced seeds = {seeds}")

        maps_classes = [
            Seed2Soil,
            Soil2Fertilizer,
            Fertilizer2Water,
            Water2Light,
            Light2Temperature,
            Temperature2Humidity,
            Humidity2Location,
        ]
        maps = {}

        while "map" not in next(iterable, None):
            pass

        for map_class in maps_classes:
            logger.trace(f"Extracting {map_class.__name__} maps.")
            maps[map_class.__name__] = []
            while (line := next(iterable, None)) is not None:
                logger.trace(f"Processing line: {line}")
                if line == "":
                    continue
                if "map" in line:
                    break
                maps[map_class.__name__].append(map_class(*extract_numbers(line)))
            logger.trace(f"Line after while loop. [{line=}, {map_class=}]")
            logger.debug(f"Extracted maps {map_class.__name__} = {maps[map_class.__name__]}")

        return cls(
            seeds=seeds,
            seed_to_soil=maps[Seed2Soil.__name__],
            soil_to_fertilizer=maps[Soil2Fertilizer.__name__],
            fertilizer_to_water=maps[Fertilizer2Water.__name__],
            water_to_light=maps[Water2Light.__name__],
            light_to_temperature=maps[Light2Temperature.__name__],
            temperature_to_humidity=maps[Temperature2Humidity.__name__],
            humidity_to_location=maps[Humidity2Location.__name__],
        )

    def find_location(self, seed: Seed) -> int:
        src = seed.id

        for key, map_list in self.maps.items():
            logger.trace(f"Finding dst for {src=} in {key}.")
            dst = None
            for map in map_list:
                logger.trace(f"Finding dst for {src=} in {map}.")
                dst = map.map_int_from_src_to_dst(src)
                if dst is not None:
                    break
            if dst is None:
                dst = src
            logger.debug(f"Mapped {src=} to {dst=} in {key}.")
            src = dst
        logger.info(f"{seed=} mapped to destination {src:,d}.")
        return src

    def find_closest_location(self) -> int:
        return min((self.find_location(seed) for seed in self.seeds))

    def map_seed_ranges(self):
        results = []
        untouched = [SeedRange(start.id, size.id) for start, size in pairwise(self.seeds)]
        logger.debug(f"Computed seed ranges from input data. [{untouched}]")
        for key, map_list in self.maps.items():
            logger.debug(f"Going through all {key} maps.")
            mapped = []
            for map in map_list:
                logger.debug(f"Mapping input range {untouched=} through {map=}")
                new_mapped, new_untouched = map.map_ranges(untouched)
                logger.debug(f"Got {mapped=} and {untouched=} from {map=}.")
                mapped.extend(new_mapped)
                untouched = new_untouched
            untouched = mapped + untouched
        return untouched


def process_input(iterable) -> int:
    almanac = Almanac.parse_input(iterable)
    return min(almanac.map_seed_ranges()).start

@logger.catch
def main(input):
    if input is None:
        input = os.path.join(os.path.dirname(__file__), "./input")
    possible_games = []
    with open(input, "r") as f:
        total = process_input((line.strip() for line in f.readlines()))
        logger.warning(f"Solution is: {total:,d} ({total})")
    return total


if __name__ == "__main__":
    input = sys.argv[1] if len(sys.argv) == 2 else None
    main(input)


TEST_INPUT = (line.strip() for line in """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".split("\n") if line.strip())

@pytest.fixture(scope="module")
def almanac():
    return Almanac.parse_input(TEST_INPUT)

def test_parse_input(almanac):
    assert almanac.seeds == [Seed(79), Seed(14), Seed(55), Seed(13)]
    # assert almanac.seed_to_soil == [Seed2Soil(50, 98, 2), Seed2Soil(52, 50, 48)]
    assert almanac.maps["seed_to_soil"] == [Seed2Soil(50, 98, 2), Seed2Soil(52, 50, 48)]
    # etc. I'm lazy

def test_map(almanac):
    assert almanac.maps["seed_to_soil"][0].map_int_from_src_to_dst(97) is None
    assert almanac.maps["seed_to_soil"][0].map_int_from_src_to_dst(98) == 50
    assert almanac.maps["seed_to_soil"][0].map_int_from_src_to_dst(99) == 51
    assert almanac.maps["seed_to_soil"][0].map_int_from_src_to_dst(100) is None

    assert almanac.maps["seed_to_soil"][1].map_int_from_src_to_dst(53) == 55

    assert almanac.maps["soil_to_fertilizer"][0].map_int_from_src_to_dst(15) == 0
    assert almanac.maps["soil_to_fertilizer"][0].map_int_from_src_to_dst(51) == 36
    assert almanac.maps["soil_to_fertilizer"][0].map_int_from_src_to_dst(14) is None
    assert almanac.maps["soil_to_fertilizer"][0].map_int_from_src_to_dst(52) is None

def test_find_location(almanac):
    assert almanac.find_location(Seed(79)) == 82
    assert almanac.find_location(Seed(14)) == 43
    assert almanac.find_location(Seed(55)) == 86
    assert almanac.find_location(Seed(13)) == 35


def test_test_input(almanac):
    assert almanac.find_closest_location() == 35

def test_range_contains():
    range_5_10 = Range(5, 6)
    assert range_5_10.start == 5
    assert range_5_10.end == 10

    assert 4 not in range_5_10
    assert 5 in range_5_10
    assert 10 in range_5_10
    assert 11 not in range_5_10

    range_4_11 = Range(4, 8)
    assert range_4_11.start == 4
    assert range_4_11.end == 11

    range_4_12 = Range(4, 9)
    assert range_4_12.start == 4
    assert range_4_12.end == 12
    assert range_4_11 in range_4_12
    assert range_4_12 not in range_4_11

def test_split_range():
    range_5_10 = Range(5, 6)
    range_4_11 = Range(4, 8)

    ranges = range_5_10.split_range(range_4_11)
    assert ranges == [
        Range(4, 1),
        Range(5, 6),
        Range(11, 1)
    ]

    assert range_5_10.split_range(Range(7, 1)) == [Range(7, 1)]

def test_map_range_known_result(almanac):
    almanac.seeds = [Seed(82), Seed(1)]
    mapped_ranges = almanac.map_seed_ranges()
    assert mapped_ranges == [Range(46, 1)]

def test_map_range(almanac):
    mapped_ranges = almanac.map_seed_ranges()
    assert min(mapped_ranges).start == 46

def test_solve_part_two():
    assert main(None) == 6472060
