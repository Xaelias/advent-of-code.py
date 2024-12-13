import numpy as np
from loguru import logger


def quadratic_solve(
    x: float,
    *args: tuple[int, int],
):
    coeffs, results = zip(*args)
    coeffs_matrix = np.array([[x**2, x, 1] for x in coeffs])
    logger.trace(f"Generated coffs matrix: {coeffs_matrix}")
    a, b, c = np.linalg.solve(coeffs_matrix, results)
    logger.debug(f"Solved {a=} {b=} {c=}")
    return a * x**2 + b * x + c


# for a system that's:
# 23 * x + 42 y = 78
# 31 * x + 87 y = -3
# coeffs = [[23, 42], [31, 87]]
# results = [78, -3]
def numpy_system(coeffs: list[list[float | int]], results: list[float | int]) -> list[float]:
    return np.linalg.solve(coeffs, results)


# a1 * x + b1 * y = c1
# a2 * x + b2 * y = c2
def fast_dual_system(
    a1: float,
    b1: float,
    c1: float,
    a2: float,
    b2: float,
    c2: float,
) -> list[float]:
    try:
        y = ((a1 * c2) - (a2 * c1)) / ((a1 * b2) - (a2 * b1))
        x = (c1 - (b1 * y)) / a1
        return [x, y]
    except Exception:
        # just defaulting back because I'm lazy and don't want to tackle all the special cases
        return numpy_system(
            [
                [a1, b1],
                [a2, b2],
            ],
            [c1, c2],
        )
