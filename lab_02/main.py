from cmath import nan
import scipy
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d


def get_polynomial_degree():
    nx, ny, nz = map(int, input("Input polynomials degrees: ").split())
    return nx, ny, nz


def get_x_line(data, arr):
    print(data)
    for i in range(len(data) - 1):
        arr[i] = data[i]

def get_data(linesz, linesx, linesy):
    file = open("2.txt")
    table_lines = [line.strip() for line in file]
    z = 0
    coly = 5
    ys = []
    nnum = []
    nnnum = []
    for line in table_lines:
        if line == "":
            nnnum.append(nnum)
            nnum = []
        elif "z=" in line:
            z = float(line[list(line).index("=") + 1])
            linesz.append(z)
        elif "y" in line:
            xs = list(map(float, line[3:].split()))
            linesx.append(xs)
        else:
            linesnum = list(map(float, line.split()))
            nnum.append(linesnum)
            y = linesnum[0]
            ys.append(y)
            if (len(ys) == coly):
                linesy.append(ys)
                ys = []
            linesnum.pop(0)
    nnnum.append(nnum)
    return nnnum, linesy, linesz


def getNearCoef(arr, xMean):
    for i in range(len(arr)):
        if arr[i] > xMean:
            return i

def getFirstColumnTable(arr, n, coef):
    start = 0
    end = 0
    if (coef - n // 2 >= 0):
        start = coef - n// 2
    if (start == 0):
        end = n + 1
    else:
        end = coef + n // 2 + n % 2 + 1
        if (end > n):
            start -= (end - n - 2) 
            end = n + 1
    arr_copy = []
    #print(coef, start, end)
    for i in range(start, end):
        arr_copy.append(arr[i])
    
    return arr_copy


def create_n_table(z, y, x, nx, ny, nz, xMean, yMean, zMean):
    table = np.zeros([nz + 1, ny + 1, nx + 1])
    for i in range(nz + 1):
        for j in range(ny + 1):
            coef = getNearCoef(x[i][j], xMean)
            arr = getFirstColumnTable(x[i][j], nx + 1, coef)
            for k in range(nx + 1):
                table[i][j][k] = arr[k]
    linesy = np.zeros([nz + 1, ny + 1])
    for i in range(nz + 1):
        coef = getNearCoef(y[i], yMean)
        arr = getFirstColumnTable(y[i], ny + 1, coef)
        for j in range(ny + 1):
            linesy[i][j] = arr[j]
    linesz = np.zeros(nz + 1)
    coef = getNearCoef(z, zMean)
    arr = getFirstColumnTable(z, nz + 1, coef)
    for i in range(nz + 1):
        linesz[i] = arr[i]
    return table, linesy, linesz


def getDivededDiff(x, y, n):
    table = np.zeros([n, n])
    table[:,0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x[i + j] - x[i])
    data = pd.DataFrame(data=table)
    #print(data)
    return table

def getNewtonPoly(table, x, xMean, n):
    yx = table[0]
    p = xMean - x[0]
    for i in range(1, n):
        yx += table[i] * p
        p *= xMean - x[i]
    return yx

def get_answer(x, z, y, nx, ny, nz, xMean, yMean, zMean):
    #print(x)
    #print(y)
    #print(z)
    yInter = np.zeros([nz + 1, ny + 1])
    for i in range(0, nz + 1):
        for j in range(0 , ny + 1):
            table = getDivededDiff(x[i][j], y[i], nx + 1)[0, :]
            yInter[i][j] = getNewtonPoly(table, x[i][j], xMean, nx + 1)
    print(yInter)
    zInter = []
    for i in range(nz + 1):
        table = getDivededDiff(y[i], yInter[i], ny + 1)[0, :]
        zInter.append(getNewtonPoly(table, y[i], yMean, ny + 1))
    print(zInter)
    table = getDivededDiff(z, zInter, nz + 1)[0, :]
    res = getNewtonPoly(table, z, zMean, nz + 1)
    return res
    

if __name__ == '__main__':
    nx, ny, nz = get_polynomial_degree()
    xMean, yMean, zMean = map(float, input("Input x, y, z: ").split())
    linesz, linesx, linesy = [], [], []
    table, linesy, linesz = get_data(linesz, linesx, linesy)
    table, linesy, linesz = create_n_table(linesz, linesy, table, nx, ny, nz, xMean, yMean, zMean)
    print(get_answer(table, linesz, linesy, nx, ny, nz, xMean, yMean, zMean))