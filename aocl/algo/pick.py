from shapely.geometry import Polygon

from aocl.p2 import P2

RULD = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def go_direction(position: P2, direction: str, times: int):
    offset = RULD["RULD".index(direction)]
    return position[0] + times * offset[0], position[1] + times * offset[1]


class Pick:
    @classmethod
    def area_from_xy_tuples(cls, xy: list[P2]) -> int:
        poly = Polygon(xy)
        return int(poly.area + poly.length / 2) + 1

    @classmethod
    def area_from_positions_list(cls, coordinates: list[P2]) -> int:
        return cls.area_from_xy_tuples(coordinates)

    @classmethod
    def area_from_direction_distance_tuples(cls, dir_dist: list[tuple[str, int]]) -> int:
        pos = (0, 0)
        coordinates = [pos]
        for direction, distance in dir_dist:
            pos = go_direction(pos, direction, distance)
            coordinates.append(pos)
        return cls.area_from_positions_list(coordinates)
