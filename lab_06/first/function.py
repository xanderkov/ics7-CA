from math import sqrt
from gauss import gauss_integrate
from simpson import simpson_integrate

def function(n: int, m: int) -> float:
    def f1(y):
        def f(x):
            return sqrt(x * x + y * y)
        x1 = 1 - sqrt(1 - y * y)
        x2 = 1 + sqrt(1 - y * y)
        return simpson_integrate(f, x1, x2, m)
    return gauss_integrate(f1, -1, 1, n)
