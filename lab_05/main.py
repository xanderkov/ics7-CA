import numpy as np
from function import *
import matplotlib.pyplot as plt

h = l / N

def Afunc(kprev, kcur):
    return (kprev + kcur) / 2

def Bfunc(kprev, kcur, knext, p, h):
    return (kprev + kcur) / 2 + (kcur + knext) / 2 + p * h**2

def Cfunc(kcur, knext):
    return (kcur + knext) / 2

def Dfunc(f, h):
    return f * h**2

def Aprev_deriv(yprev):
    return 0.5 * a1 * c1 * m1 * yprev**(m1 - 1)

def Bprev_deriv(yprev):
    return 0.5 * a1 * c1 * m1 * yprev**(m1 - 1)

def Acur_deriv(ycur):
    return 0.5 * a1 * c1 * m1 * ycur**(m1 - 1)

def Bcur_deriv(ycur):
    return a1 * c1 * m1 * ycur**(m1 - 1) + 8 * h**2 * alpha0 / (delta * R) * (ycur/delta - 1)**3

def Ccur_deriv(ycur):
    return 0.5 * a1 * c1 * m1 * ycur**(m1 - 1)

def Dcur_deriv(ycur):
    return h**2 * 8 * T0 * alpha0 / (delta * R) * (ycur / delta - 1)**3

def Bnext_deriv(ynext):
    return 0.5 * a1 * c1 * m1 * ynext**(m1 - 1)

def Cnext_deriv(ynext):
    return 0.5 * a1 * c1 * m1 * ynext**(m1 - 1)

def task_1():
    # Сеточная функция
    x = np.linspace(0, l, num=(N + 1), endpoint=True)
    y = np.zeros(len(x)) + T0 # начальное приближение

    cur_e = float("inf")
    while (cur_e >= e):
        Coef = list()
        Coef.append([0,
                     (k(y[0]) + k(y[1])) / 2 + p(y[0]) * h**2,
                     (k(y[0]) + k(y[1])) / 2,
                     f(y[0]) * h**2 + F0 * h])

        for i in range(1, N):
            Ai = Afunc( k(y[i - 1]), k(y[i]) )
            Bi = Bfunc( k(y[i - 1]), k(y[i]), k(y[i + 1]), p(y[i]), h )
            Ci = Cfunc( k(y[i]), k(y[i + 1]) )
            Di = Dfunc( f(y[i]), h )
            Coef.append([Ai, Bi, Ci, Di])

        Coef.append([(k(y[N - 1]) + k(y[N])) / 2,
                     (k(y[N - 1]) + k(y[N])) / 2 + p(y[N]) * h**2 + alpha(y[N]) * h,
                     0,
                     f(y[N]) * h**2 + alpha(y[N]) * T0 * h])

        Linear_coef = list()
        Linear_coef.append([0,
                            Bcur_deriv(y[0]) * y[0] + Coef[0][1] - Ccur_deriv(y[1]) * y[1] - Dcur_deriv(y[0]),
                            -Bnext_deriv(y[0]) * y[0] + Cnext_deriv(y[1]) * y[1] + Coef[0][2],
                            -Coef[0][1] * y[0] + Coef[0][2] * y[1] + Coef[0][3]])

        for i in range(1, N):
            Ai = Coef[i][0]; Bi = Coef[i][1]; Ci = Coef[i][2]; Di = Coef[i][3]
            Di_derivative = Ai * y[i - 1] - Bi * y[i] + Ci * y[i + 1] + Di
            Ai_derivative = Aprev_deriv(y[i - 1]) * y[i - 1] + Ai - Bprev_deriv(y[i - 1]) * y[i]
            Bi_derivative = -(Acur_deriv(y[i]) * y[i - 1] - Bcur_deriv(y[i]) * y[i] - Bi + Ccur_deriv(y[i]) * y[i + 1] + Dcur_deriv(y[i]))
            Ci_derivative = -Bnext_deriv(y[i + 1]) * y[i] + Cnext_deriv(y[i + 1]) * y[i + 1] + Ci
            Linear_coef.append(np.array([Ai_derivative, Bi_derivative, Ci_derivative, Di_derivative]))

        Linear_coef.append([Aprev_deriv(y[N - 1]) * y[N - 1] + Coef[N][0] - Bprev_deriv(y[N - 1]) * y[N],
                            -Acur_deriv(y[N]) * y[N - 1] + Bcur_deriv(y[N]) * y[N] + Coef[N][1] - Dcur_deriv(y[N]),
                            0,
                            Coef[N][0] * y[N - 1] - Coef[N][1] * y[N] + Coef[N][3]])

        ksi = list([0])
        eta = list([0])
        for i in range(1, N + 1):
            C = Linear_coef[i - 1][2]
            B = Linear_coef[i - 1][1]
            A = Linear_coef[i - 1][0]
            D = Linear_coef[i - 1][3]

            ksi.append(C / (B - A * ksi[i - 1]))
            eta.append((A * eta[i - 1] + D) / (B - A * ksi[i - 1]))

        deltay = list([(Linear_coef[N][0] * eta[N] + Linear_coef[N][3])
                        / (Linear_coef[N][1] - Linear_coef[N][0] * ksi[N])])
        for i in range(N - 1, -1, -1):
            deltay.insert(0, ksi[i + 1] * deltay[0] + eta[i + 1])

        maxdiv = -1
        for i in range(0, N + 1):
            division = abs(deltay[i] / y[i])
            maxdiv = max(maxdiv, division)
        cur_e = maxdiv
        print(cur_e)

        for i in range(0, N + 1):
            y[i] += deltay[i]

    plt.plot(x, y, color="r")

    plt.title("Задание 1")
    plt.show()

    return [x, y]


if __name__ == '__main__':
    task_1()