from dataclasses import dataclass
from itertools import combinations
from typing import Any

from shapely import LineString

from aocl.base import AoCInput
from aocl.base import Base


@dataclass
class Hail:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int


class Solution(Base):
    @classmethod
    def parse(cls, input_data: AoCInput) -> Any:
        r = []
        for line in input_data.as_list_of_str:
            px, py, pz, vx, vy, vz = map(int, line.replace(" @ ", ", ").split(", "))
            r.append(Hail(px, py, pz, vx, vy, vz))
        return r

    @classmethod
    def process_part_one(
        cls,
        parsed_input: Any,
        range_start: int = int(2e14),
        range_stop: int = int(4e14),
        **kwargs: Any,
    ) -> int | str:
        lines = []
        for hail in parsed_input:
            # simply solving for t (for both x and y):
            #   x + t1 * dx == range_start
            #   x + t2 * dx == range_stop
            x_times = sorted([(range_start - hail.x) / hail.dx, (range_stop - hail.x) / hail.dx])
            y_times = sorted([(range_start - hail.y) / hail.dy, (range_stop - hail.y) / hail.dy])

            # if max time is < 0, we're never in the range:
            if x_times[1] < 0 or y_times[1] < 0:
                continue

            t1 = max(x_times[0], y_times[0], 0)  # we can't go back in time
            t2 = min(x_times[1], y_times[1])

            # from there we can find the lines:
            x_t1 = hail.x + hail.dx * t1
            y_t1 = hail.y + hail.dy * t1
            x_t2 = hail.x + hail.dx * t2
            y_t2 = hail.y + hail.dy * t2

            lines.append((hail, LineString([(x_t1, y_t1), (x_t2, y_t2)])))

        return sum(line_1[1].intersects(line_2[1]) for line_1, line_2 in combinations(lines, 2))

    @classmethod
    def process_part_two(cls, parsed_input: Any, **kwargs: Any) -> int | str:
        # sympy
        import sympy

        x, y, z, dx, dy, dz = map(sympy.symbols, ("x", "y", "z", "dx", "dy", "dz"))
        t = sympy.symbols("t(:3)")
        equations = []
        for i, hail in enumerate(parsed_input[:3]):
            equations.append(x + t[i] * dx - (hail.x + hail.dx * t[i]))
            equations.append(y + t[i] * dy - (hail.y + hail.dy * t[i]))
            equations.append(z + t[i] * dz - (hail.z + hail.dz * t[i]))
        return sum(sympy.solve(equations, (x, y, z, dx, dy, dz, *t))[0][:3])

        # other way of writing the samet thing
        # hail = parsed_input
        # p, v, t = map(sympy.symbols, (f"{c}(:3)" for c in "pvt"))
        # equations = [
        #     p[axis] + t[idx] * v[axis] - (h[axis] + h[axis + 3] * t[idx])
        #     for idx in range(3)
        #     for axis in range(3) if (h := astuple(hail[idx]))
        # ]
        # return sum(sympy.solve(equations, (*p, *v, *t))[0][:3])

        # Z3 (slower)
        # import z3
        # solver = z3.Solver()
        # x, y, z, dx, dy, dz = map(z3.Int, ("x", "y", "z", "dx", "dy", "dz"))
        #
        # for i, hail in enumerate(parsed_input[:3]):
        #     ti = z3.Int(f"t{i}")
        #     solver.add(x + dx * ti == hail[0] + hail[3] * ti)
        #     solver.add(y + dy * ti == hail[1] + hail[4] * ti)
        #     solver.add(z + dz * ti == hail[2] + hail[5] * ti)
        # solver.check()
        # return solver.model().eval(x + y + z)
