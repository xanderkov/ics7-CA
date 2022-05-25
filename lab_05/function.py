from const import *

def alpha(T):
    return alpha0 * (T / delta - 1)**4 + gamma

def p(T):
    return 2 * alpha(T) / R

def f(T):
    return 2 * T0 / R * alpha(T)

def k(T):
    return a1 * (b1 + c1 * T**m1)

if __name__ == '__main__':
    pass