from cmath import nan
import scipy
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re


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


def create_n_table(z, y, x, nx, ny, nz):
    table = np.zeros([nz + 1, ny + 1, nx + 1])
    for i in range(nz + 1):
        for j in range(ny + 1):
            for k in range(nx + 1):
                table[i][j][k] = x[i][j][k]
    linesy = np.zeros([nz + 1, ny + 1])
    for i in range(nz + 1):
        for j in range(ny + 1):
            linesy[i][j] = y[i][j]
    linesz = np.zeros(nz + 1)
    for i in range(nz + 1):
        linesz[i] = z[i]
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
    print(z, zInter)
    table = getDivededDiff(z, zInter, nz + 1)[0, :]
    res = getNewtonPoly(table, z, zMean, nz + 1)
    return res
    

if __name__ == '__main__':
    nx, ny, nz = get_polynomial_degree()
    xMean, yMean, zMean = map(int, input("Input x, y, z: ").split())
    linesz, linesx, linesy = [], [], []
    table, linesy, linesz = get_data(linesz, linesx, linesy)
    table, linesy, linesz = create_n_table(linesz, linesy, table, nx, ny, nz)
    print(get_answer(table, linesz, linesy, nx, ny, nz, xMean, yMean, zMean))