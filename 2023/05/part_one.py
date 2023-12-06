#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Alexis Lesieur
# Date              : 2023/12/05 15:28:00
# Last Modified Date: 2023/12/05 17:52:23
# Last Modified By  : Alexis Lesieur
import os
import pytest
import re
import sys

from collections import OrderedDict
from loguru import logger
from typing import Optional


class Seed:
    def __init__(self, id: int):
        self.id = id

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"

    def __eq__(self, other):
        return self.id == other.id

class AlmanacMap:
    def __init__(self, dst_start: int, src_start: int, size: int):
        self.dst_start = dst_start
        self.src_start = src_start
        self.size = size

    def __repr__(self):
        return f"<{self.__class__.__name__}: src_start={self.src_start}, dst_start={self.dst_start}, size={self.size}>"

    def __eq__(self, other):
        return self.src_start == other.src_start and self.dst_start == other.dst_start and self.size == other.size

    def find_dst(self, src: int) -> Optional[int]:
        logger.trace(f"{self=} - trying to find mapping for {src}")
        if src < self.src_start or src >= self.src_start + self.size:
            return None
        else:
            return self.dst_start + (src - self.src_start)

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
        # self.seed_to_soil = seed_to_soil
        # self.soil_to_fertilizer = soil_to_fertilizer
        # self.fertilizer_to_water = fertilizer_to_water
        # self.water_to_light = water_to_light
        # self.light_to_temperature = light_to_temperature
        # self.temperature_to_humidity = temperature_to_humidity
        # self.humidity_to_location = humidity_to_location
        self.maps = OrderedDict([
            ("seed_to_soil", seed_to_soil),
            ("soil_to_fertilizer", soil_to_fertilizer),
            ("fertilizer_to_water", fertilizer_to_water),
            ("water_to_light", water_to_light),
            ("light_to_temperature", light_to_temperature),
            ("temperature_to_humidity", temperature_to_humidity),
            ("humidity_to_location", humidity_to_location),
        ])

    def find_location(self, seed: Seed) -> int:
        src = seed.id

        for key, map_list in self.maps.items():
            logger.trace(f"Finding dst for {src=} in {key}.")
            dst = None
            for map in map_list:
                logger.trace(f"Finding dst for {src=} in {map}.")
                dst = map.find_dst(src)
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


    def __repr__(self):
        return f"<{self.__class__.__name__}: seeds: {', '.join(self.seeds)}>"

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
                maps[map_class.__name__].append(Seed2Soil(*extract_numbers(line)))
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


def extract_numbers(line: str) -> list[int]:
    logger.trace(f"Extracing numbers from line: {line}")
    matches = re.findall(r"\d+", line)
    logger.trace(f"Extracted numbers from line. [{line=}, {matches=}]")
    return [int(match) for match in matches]


def process_input(iterable) -> int:
    almanac = Almanac.parse_input(iterable)
    return almanac.find_closest_location()

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
    logger.warning(f"Parsing test input")
    return Almanac.parse_input(TEST_INPUT)

def test_parse_input(almanac):
    assert almanac.seeds == [Seed(79), Seed(14), Seed(55), Seed(13)]
    # assert almanac.seed_to_soil == [Seed2Soil(50, 98, 2), Seed2Soil(52, 50, 48)]
    assert almanac.maps["seed_to_soil"] == [Seed2Soil(50, 98, 2), Seed2Soil(52, 50, 48)]
    # etc. I'm lazy

def test_find_dst(almanac):
    assert almanac.maps["seed_to_soil"][0].find_dst(97) is None
    assert almanac.maps["seed_to_soil"][0].find_dst(98) == 50
    assert almanac.maps["seed_to_soil"][0].find_dst(99) == 51
    assert almanac.maps["seed_to_soil"][0].find_dst(100) is None

    assert almanac.maps["seed_to_soil"][1].find_dst(53) == 55

    assert almanac.maps["soil_to_fertilizer"][0].find_dst(15) == 0
    assert almanac.maps["soil_to_fertilizer"][0].find_dst(51) == 36
    assert almanac.maps["soil_to_fertilizer"][0].find_dst(14) is None
    assert almanac.maps["soil_to_fertilizer"][0].find_dst(52) is None

def test_find_location(almanac):
    assert almanac.find_location(Seed(79)) == 82
    assert almanac.find_location(Seed(14)) == 43
    assert almanac.find_location(Seed(55)) == 86
    assert almanac.find_location(Seed(13)) == 35


def test_test_input(almanac):
    assert almanac.find_closest_location() == 35

# def test_full_input():
    # assert main(None) == "???"
