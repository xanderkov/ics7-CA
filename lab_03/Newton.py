import pandas as pd
import numpy as np


def get_polynomial_degree():
    nx, ny, nz = map(int, input("Input polynomials degrees: ").split())
    return nx, ny, nz
        

def findCoefIndex(line, coef):
    index = 0
    for i in range(len(line)):
        if abs(line[i] - coef) < abs(line[index] - coef):
            index = i
    return index


def findStartEndIndexes(n, index, line):
    left = index
    right = index
    for i in range(n - 1):
        if i % 2 != 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(line) - 1:
                left -= 1
            else:
                right += 1
    return line[left:right + 1]

def getnArr(coef, n, line):
    newArr = []
    index = findCoefIndex(line, coef)
    newArr = findStartEndIndexes(n + 1, index, line)
    return newArr


def sync_sort2(x, y):
    indices = sorted(range(len(x)), key=lambda i: x[i])
    x = [x[i] for i in indices]
    y = [y[i] for i in indices]
    return x, y
    
def prepare_arrays_newton(x, y, n, x0):
    need_to_take = n + 1
    if need_to_take > len(x):
        print('ОШИБКА: не хватает точек для построения полинома Ньютона')
    x, y = sync_sort2(x, y)
    closest_to_x0_i = (sorted(range(len(x)), key=lambda i: abs(x[i] - x0)))[0]
    from_i = closest_to_x0_i - need_to_take // 2 
    if from_i < 0:
        from_i = 0   
    to_i = from_i + need_to_take 
    if to_i > len(x):
        to_i = len(x)
        from_i = to_i - need_to_take  
    x_new = x[from_i : to_i]
    y_new = y[from_i : to_i]
    return x_new, y_new


def getDivededDiff(x, y, n):
    table = np.zeros([n, n])
    table[:,0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x[i + j] - x[i])
    data = pd.DataFrame(data=table)
    #print(data)
    return table[0, :]

def getNewtonPoly(table, x, xMean, n):
    n = n - 1
    p = table[n]
    for k in range(1, n + 1):
        p = table[n - k] + (xMean - x[n - k]) * p
    return p

def getNewtonDif2(table, x, x0, n):
    a = 2 * table[1] + 2 * table[2] * (x0 - x[0]) + 2 * table[2] * (2 * x0 - x[1] - x[2])
    b = 2 * (2 * x0 - x[2] - x[3]) * (table[3] * (x0 - x[0]) + table[3] * (x0 - x[1]))
    c = 2 * table[3] * (x0 - x[0]) * (x0 - x[1])
    d = 2 * table[3] * (x0 - x[2]) * (x0 - x[3])
    return  a + b + c + d


def makeNewtonAprox(x, y, n, x0):
    x_new, y_new = prepare_arrays_newton(x, y, n, x0)
    coef = getDivededDiff(x_new, y_new, n + 1)
    return getNewtonPoly(coef, x_new, x0, n + 1)

def makeNewtonAproxDif2(x, y, n, x0):
    n = 3
    x_new, y_new = prepare_arrays_newton(x, y, n, x0)
    coef = getDivededDiff(x_new, y_new, n + 1)
    return getNewtonDif2(coef, x_new, x0, n + 1)