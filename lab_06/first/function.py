DELTA = 1e-7


def f(x, y):
    if (x - 1) ** 2 + y ** 2 - 1 > DELTA:
        return 0
    else:
        return (x ** 2 + y ** 2) ** 0.5
