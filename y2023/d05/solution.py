import re
from collections import OrderedDict
from typing import Any
from typing import Iterator
from typing import Optional
from typing import Self

from loguru import logger

from aocl.base import AoCInput
from aocl.base import Base


class Seed:
    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.idx}>"

    def __eq__(self, other):
        return self.idx == other.idx


class SeedRange:
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

    def __contains__(self, other) -> bool:
        logger.trace(f"Testing if {other=} in {self=}.")
        if isinstance(other, int):
            return self.start <= other <= self.end
        if isinstance(other, self.__class__):
            return self.start <= other.start and other.end <= self.end
        return False

    def touches(self, other: Self) -> bool:
        return self.start in other or self.end in other or other.start in self or other.end in self

    def split_range(self, other: Self) -> list["SeedRange"]:
        logger.trace(f"Testing if {other=} intersect with {self=}")
        if other.size == 1:
            logger.trace("Input is of size one, nothing to do")
            return [other]
        if not self.touches(other):
            logger.trace("Skiping computing intersection of distinct ranges.")
            return [other]

        limits = [
            e
            for e in sorted(list({self.start, self.end, other.start, other.end}))
            if other.start <= e <= other.end
        ]
        logger.trace(f"Found limits. [{self=}, {other=}, {limits=}]")
        ranges = []
        prev_limit = limits[0]
        for next_limit in limits[1:]:
            if prev_limit not in self and next_limit not in self:
                # exclusively after self
                new_range = SeedRange(prev_limit, next_limit - prev_limit + 1)
                prev_limit = next_limit
            elif prev_limit not in self:
                # before self
                new_range = SeedRange(prev_limit, next_limit - prev_limit)
                logger.trace(
                    f"Computing range where prev not in self. [{self=}, {prev_limit=}, {next_limit=}, {new_range=}]"
                )
                prev_limit = next_limit
            else:
                # in self
                new_range = SeedRange(prev_limit, next_limit - prev_limit + 1)
                logger.trace(
                    f"Computing range where prev in self. [{self=}, {prev_limit=}, {next_limit=}, {new_range=}]"
                )
                prev_limit = next_limit + 1
            ranges.append(new_range)
        return ranges


class AlmanacMap:
    def __init__(self, dst_start: int, src_start: int, size: int):
        self.src = SeedRange(src_start, size)
        self.dst = SeedRange(dst_start, size)
        self.size = size

    def __repr__(self):
        return f"<{self.__class__.__name__}: src={self.src}, dst={self.dst}, size={self.size}>"

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst and self.size == other.size

    def find_dst(self, src: int) -> Optional[int]:
        if src not in self.src:
            return None
        return self.dst.start + (src - self.src.start)

    def map_int_from_src_to_dst(self, src: int) -> Optional[int]:
        logger.trace(f"{self=} - trying to find mapping for {src}")
        if src in self.src:
            return (src - self.src.start) + self.dst.start
        return None

    def map_range(self, r: SeedRange) -> tuple[list[SeedRange], list[SeedRange]]:
        logger.trace(f"Mapping a single range. [{self=}, {r=}]")
        mapped = []
        untouched = []
        for r in self.src.split_range(r):
            logger.trace(f"Processing one intersection. [{self=}, {r=}]")
            if r in self.src:
                mapped.append(SeedRange(self.dst.start + (r.start - self.src.start), r.size))
                logger.trace(f"New mapped range. [{self=}, {mapped[-1]=}]")
            else:
                untouched.append(r)
                logger.trace(f"New untouched range. [{self=}, {untouched[-1]=}]")
        return mapped, untouched

    def map_ranges(self, ranges: list[SeedRange]) -> tuple[list[SeedRange], list[SeedRange]]:
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
        self.maps = OrderedDict(
            [
                ("seed_to_soil", seed_to_soil),
                ("soil_to_fertilizer", soil_to_fertilizer),
                ("fertilizer_to_water", fertilizer_to_water),
                ("water_to_light", water_to_light),
                ("light_to_temperature", light_to_temperature),
                ("temperature_to_humidity", temperature_to_humidity),
                ("humidity_to_location", humidity_to_location),
            ]
        )

    def find_location(self, seed: Seed) -> int:
        src = seed.idx

        for key, map_list in self.maps.items():
            dst = None
            for almap in map_list:  # type: ignore
                dst = almap.find_dst(src)
                if dst is not None:
                    break
            if dst is None:
                dst = src
            src = dst
        return src

    def find_closest_location(self) -> int:
        return min((self.find_location(seed) for seed in self.seeds))

    @classmethod
    def parse_input(cls, iterable: Iterator[str]) -> Self:
        line = next(iterable)
        seeds = [Seed(int(i)) for i in re.findall(r"\d+", line)]

        maps_classes = [
            Seed2Soil,
            Soil2Fertilizer,
            Fertilizer2Water,
            Water2Light,
            Light2Temperature,
            Temperature2Humidity,
            Humidity2Location,
        ]
        maps: dict[str, list[Any]] = {}

        while "map" not in next(iterable, None):  # type: ignore
            pass

        for map_class in maps_classes:
            maps[map_class.__name__] = []
            while (line := next(iterable, None)) is not None:  # type: ignore
                if line == "":
                    continue
                if "map" in line:
                    break
                maps[map_class.__name__].append(Seed2Soil(*extract_numbers(line)))

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

    def map_seed_ranges(self):
        untouched = [SeedRange(start.idx, size.idx) for start, size in pairwise(self.seeds)]
        logger.debug(f"Computed seed ranges from input data. [{untouched}]")
        for key, map_list in self.maps.items():
            logger.debug(f"Going through all {key} maps.")
            mapped = []
            for almap in map_list:
                logger.debug(f"Mapping input range {untouched=} through {almap=}")
                new_mapped, new_untouched = almap.map_ranges(untouched)
                logger.debug(f"Got {mapped=} and {untouched=} from {almap=}.")
                mapped.extend(new_mapped)
                untouched = new_untouched
            untouched = mapped + untouched
        return untouched


def extract_numbers(line: str) -> list[int]:
    matches = re.findall(r"\d+", line)
    return [int(match) for match in matches]


def process_input(iterable) -> int:
    almanac = Almanac.parse_input(iterable)
    return almanac.find_closest_location()


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        return Almanac.parse_input(input_data.as_iter)

    @classmethod
    def process_part_one(cls, parsed_input: Almanac, **kwargs: Any) -> int:
        return parsed_input.find_closest_location()

    @classmethod
    def process_part_two(cls, parsed_input: Almanac, **kwargs: Any) -> int:
        return min(parsed_input.map_seed_ranges()).start
