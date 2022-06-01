from typing import Callable as func


def simpson_integrate(f: func, a: float, b: float, n: int) -> float:
    h, res = (b - a) / n, 0
    for i in range(0, n, 2):
        x1, x2, x3 = i * h, (i + 1) * h, (i + 2) * h
        f1, f2, f3 = f(x1), f(x2), f(x3)
        res += f1 + 4 * f2 + f3
    return h / 3 * res
