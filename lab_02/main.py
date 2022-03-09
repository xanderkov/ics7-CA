import pandas as pd
import numpy as np


def get_polynomial_degree():
    nx, ny, nz = map(int, input("Input polynomials degrees: ").split())
    return nx, ny, nz


def get_data(zArr, xArr, yArr):
    file = open("2.txt")
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
    start = 0
    end = 0
    if (index - n // 2 >= 0):
        start = index - n // 2
    if (start == 0):
        end = n + 1
    else:
        end = index + n // 2 + n % 2 + 1
    if (end > len(line)):
        end = n + 1
        start = end - n - 1
    return start, end

def getnArr(coef, n, line):
    newArr = []
    index = findCoefIndex(line, coef)
    start, end = findStartEndIndexes(n, index, line)
    for i in range(start, end):
        newArr.append(line[i])
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

def get_answer(x, z, y, nx, ny, nz, xMean, yMean, zMean):
    #print(x)
    #print(y)
    #print(z)
    yInter = np.zeros([nz + 1, ny + 1])
    for i in range(0, nz + 1):
        for j in range(0 , ny + 1):
            table = getDivededDiff(y[i], x[i][j], nx + 1)[0, :]
            yInter[i][j] = getNewtonPoly(table, y[i], xMean, nx + 1)
    data = pd.DataFrame(data=yInter)
    print(data)
    zInter = []
    for i in range(nz + 1):
        table = getDivededDiff(y[i], yInter[i], ny + 1)[0, :]
        zInter.append(getNewtonPoly(table, y[i], yMean, ny + 1))
    data = pd.DataFrame(data=zInter)
    print(data)
    table = getDivededDiff(z, zInter, nz + 1)[0, :]
    res = getNewtonPoly(table, z, zMean, nz + 1)
    return res
    

if __name__ == '__main__':
    nx, ny, nz = get_polynomial_degree()
    xMean, yMean, zMean = map(float, input("Input x, y, z: ").split())
    xArr, yArr, table = [], [], []
    table, yArr, zArr = get_data(table, xArr, yArr)
    x, y, z, table = getnTable(xMean, yMean, zMean, nx, ny, nz, xArr, yArr, zArr)
    print(get_answer(table, z, y, nx, ny, nz, xMean, yMean, zMean))