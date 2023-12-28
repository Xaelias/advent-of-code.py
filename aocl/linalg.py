import numpy as np
from loguru import logger


def quadratic_solve(
    x: float,
    *args: tuple[int, int],
):
    coeffs, results = zip(*args)
    coeffs_matrix = [
        [x**2, x, 1] for x in coeffs
    ]
    logger.trace(f"Generated coffs matrix: {coeffs_matrix}")
    a, b, c = np.linalg.solve(coeffs_matrix, results)
    logger.debug(f"Solved {a=} {b=} {c=}")
    return a * x ** 2 + b * x + c
