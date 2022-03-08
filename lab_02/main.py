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
    return nnnum

def create_n_table(linesz, linesy, linesx, nx, ny, nz):
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
            nnum.append(linesnum[: nx + 1])
            y = linesnum[0]
            ys.append(y)
            if (len(ys) == coly):
                linesy.append(ys)
                ys = []
            linesnum.pop(0)
    linesz = linesz[:nz + 1]
    for i in range(len(linesy)):
        linesy[i] = linesy[i][:ny + 1]
    nnnum.append(nnum)
    return nnnum, linesy, linesz


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

def get_answer(x, z, y, nx, ny, nz):
    results = []
    for i in range(ny):
        table = getDivededDiff(x[i], y, nx)[0, :]
        results[n - 2][0] = getNewtonPoly(table, xCopy, xMean, n)
    


if __name__ == '__main__':
    nx, ny, nz = get_polynomial_degree()
    linesz, linesx, linesy = [], [], []
    table = get_data(linesz, linesx, linesy)
    linesz, linesy, linesx = [], [], []
    table, linesy, linesz = create_n_table(linesz, linesy, linesx, nx, ny, nz)
    print(get_answer(table, linesx, linesy, nx, ny, nz))