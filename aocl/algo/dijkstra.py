from heapq import heappop
from heapq import heappush
from typing import Any
from typing import Optional
from typing import Union

import numpy as np
from numpy.typing import NDArray

from aocl.p2 import RULD
from aocl.p2 import in_shape


def dijkstra(
    input_data: Union[NDArray, list[list[Any]]],
    start: tuple[int, int],
    goal: Optional[tuple[int, int]],
    min_distance: int = 1,
    max_distance: Optional[int] = None,
) -> Union[int, NDArray]:
    heap: list[tuple[int, tuple[int, int], Optional[int]]] = [(0, start, None)]

    size_x = len(input_data)
    size_y = len(input_data[0])
    costs = np.full((size_x, size_y, 4), None)

    while heap:
        cost, position, direction = heappop(heap)

        # we reached the goal
        if goal is not None and position == goal:
            return cost

        for ddidx in range(4):
            # if max_distance is set, we can't keep going in the same direction
            if max_distance is not None and ddidx == direction:
                continue
            # we can't go back
            if (ddidx + 2) % 4 == direction:
                continue
            dd = RULD[ddidx]
            cost_increase = 0
            for distance in range(1, (max_distance or 1) + 1):
                xx = position[0] + distance * dd[0]
                yy = position[1] + distance * dd[1]

                # skipping processing coordinates out of the matrix
                if not in_shape((xx, yy), (size_x, size_y)):
                    continue

                cost_increase += input_data[xx][yy]
                # skip processing coordinates if we need to move more in this direction
                if distance < min_distance:
                    continue
                cc = cost + cost_increase

                # check that we don't have already a better result for these coordinates / direction combo
                if costs[xx][yy][ddidx] is not None and costs[xx][yy][ddidx] <= cc:
                    continue

                # save current result and push coordinates / direction combo for further processing
                costs[xx][yy][ddidx] = cc
                heappush(heap, (cc, (xx, yy), ddidx if max_distance is not None else None))
    return costs
