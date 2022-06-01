from numpy import linspace, array
from numpy.linalg import solve
from typing import Callable as func
from typing import List
from math import cos, pi
from simpson import *


# Возвращает значение полинома Лежандра n-го порядка
def legendre(n: int, x: float) -> float:
    if n < 2: 
        return [1, x][n]
    P1, P2 = legendre(n - 1, x), legendre(n - 2, x)
    return ((2 * n - 1) * x * P1 - (n - 1) * P2) / n


# возвращает значение производной полинома Лежандра
def legendre_prime(n: int, x: float) -> float:
    P1, P2 = legendre(n - 1, x), legendre(n, x)
    return n / (1 - x * x) * (P1 - x * P2)


# Нахождение корней полинома Лежандра n-го порядка
def legendre_roots(n: int, eps: float = 1e-12) -> List[float]:
    roots = [cos(pi * (4 * i + 3) / (4 * n + 2)) for i in range(n)]
    for i, root in enumerate(roots):  # уточнение корней
        root_val = legendre(n, root)
        while abs(root_val) > eps:
            root -= root_val / legendre_prime(n, root)
            root_val = legendre(n, root)
        roots[i] = root
    return roots


def gauss_integ(n, m, x_left, x_right, y_bottom, y_top, function):
    t = legendre_roots(n)
    T = array([[t_i**k for t_i in t] for k in range(n)])

    int_tk = lambda k: 2 / (k + 1) if k % 2 == 0 else 0
    b = array([int_tk(k) for k in range(n)])
    A = solve(T, b)  # решение системы линейных уравнений
    s = 0
    for i in range(n):
        fun = lambda x: function(x, (y_bottom + y_top) / 2 + (y_top - y_bottom) / 2 * t[i])
        s += A[i] * simpson_integrate(fun, x_left, x_right, m)
    s *= (y_top - y_bottom) / 2
    return s
