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
        if arr[i] >= xMean:
            return i

def blcoord(c, nc, linesc):
    newc = []
    mini = abs(linesc[0] - c)
    blc = 0
    for i in range(len(linesc)):
        if abs(linesc[i] - c) < mini:
            mini = abs(linesc[i] - c)
            blc = i
    start = 0
    end = 0
    if (blc - nc // 2 >= 0):
        start = blc - nc // 2
    if (start == 0):
        end = nc + 1
    else:
        end = blc + nc // 2 + nc % 2 + 1
    if (end > len(linesc)):
        end = len(linesc)
        start = end - nc - 1
    for i in range(start, end):
        newc.append(linesc[i])
    return newc
    
def table_for_nuoton(x, y, z, nx, ny, nz):
    newz = blcoord(z, nz, linesz)
    newx = []
    for i in newz:
        newx.append(blcoord(x, nx, linesx[linesz.index(i)]))
    newy = []
    for i in newz:
        newy.append(blcoord(y, ny, linesy[linesz.index(i)]))
    
    newt = []
    for i in range(len(newz)):
        newt.append([])
        for j in range(len(newy[i])):
            newt[i].append([])
            for k in range(len(newx[i])):
                zpos = linesz.index(newz[i])
                ypos = linesy[i].index(newy[i][j])
                xpos = linesx[i].index(newx[i][k])
                newt[i][j].append(table[zpos][ypos][xpos])

    return newx, newy, newz, newt


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
    n = n -1
    p = table[n]
    for k in range(1, n + 1):
        p = table[n - k] + (xMean - x[n - k]) * p
    return p

def get_answer(x, z, y, nx, ny, nz, xMean, yMean, zMean):
    print(x)
    print(y)
    print(z)
    yInter = np.zeros([nz + 1, ny + 1])
    for i in range(0, nz + 1):
        for j in range(0 , ny + 1):
            table = getDivededDiff(y[i], x[i][j], nx + 1)[0, :]
            yInter[i][j] = getNewtonPoly(table, y[i], xMean, nx + 1)
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
    x, y, z, table = table_for_nuoton(xMean, yMean, zMean, nx, ny, nz)
    print(get_answer(table, z, y, nx, ny, nz, xMean, yMean, zMean))