import pandas as pd
import numpy as np


def get_polynomial_degree():
    nx, ny, nz = map(int, input("Input polynomials degrees: ").split())
    return nx, ny, nz


def get_data(zArr, xArr, yArr):
    file = open("1.txt")
    table_lines = [line.strip() for line in file]
    coly = 5
    ys = []
    matrix = []
    table = []
    for line in table_lines:
        if line == "":
            table.append(matrix)
            matrix = []
        elif "z=" in line:
            z = float(line[list(line).index("=") + 1])
            zArr.append(z)
        elif "y" in line:
            xs = list(map(float, line[3:].split()))
            xArr.append(xs)
        else:
            lineList = list(map(float, line.split()))
            matrix.append(lineList)
            y = lineList[0]
            ys.append(y)
            if (len(ys) == coly):
                yArr.append(ys)
                ys = []
            lineList.pop(0)
    table.append(matrix)
    return table, yArr, zArr
        

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
    
def getnTable(x, y, z, nx, ny, nz, xArr, yArr, zArr):
    newzArr = getnArr(z, nz, zArr)
    newXArr = []
    newYArr = []
    for i in newzArr:
        newXArr.append(getnArr(x, nx, xArr[zArr.index(i)]))
        newYArr.append(getnArr(y, ny, yArr[zArr.index(i)]))
    
    newTable = np.zeros([nz + 1, ny + 1, nx + 1])
    for i in range(nz + 1):
        for j in range(ny + 1):
            for k in range(nx + 1):
                zIndex = zArr.index(newzArr[i])
                yIndex = yArr[i].index(newYArr[i][j])
                xIndex = xArr[i].index(newXArr[i][k])
                newTable[i][j][k] = table[zIndex][yIndex][xIndex]

    return newXArr, newYArr, newzArr, newTable


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
    n = n - 1
    p = table[n]
    for k in range(1, n + 1):
        p = table[n - k] + (xMean - x[n - k]) * p
    return p

def get_answer(table, x, z, y, nx, ny, nz, xMean, yMean, zMean):
    print(x)
    print(y)
    print(z)
    print(table)
    zobsh = []
    for i in range(nz + 1):
        x_for_y = []
        for j in range(ny + 1):
            #print(x[i], table[i][j], nx + 1)
            trgl = getDivededDiff(x[i], table[i][j], nx + 1)[0, :]
            #print(table[i][j])
            yzn = getNewtonPoly(trgl, x[i], xMean, nx + 1)
            x_for_y.append(yzn)
        print(x_for_y)
        trgl = getDivededDiff(y[i], x_for_y, ny + 1)[0, :]
        zRes = getNewtonPoly(trgl, y[i], yMean, ny + 1)
        zobsh.append(zRes)
    print(zobsh)
    trgl = getDivededDiff(z, zobsh, nz + 1)[0, :]
    res = getNewtonPoly(trgl, z, zMean, nz + 1)
    return res
    

if __name__ == '__main__':
    nx, ny, nz = get_polynomial_degree()
    xMean, yMean, zMean = map(float, input("Input x, y, z: ").split())
    xArr, yArr, table = [], [], []
    table, yArr, zArr = get_data(table, xArr, yArr)
    x, y, z, table = getnTable(xMean, yMean, zMean, nx, ny, nz, xArr, yArr, zArr)
    print(get_answer(table, x, z, y, nx, ny, nz, xMean, yMean, zMean))