from main import *
import numpy as np

def f(x, y, z):
    return np.exp(2 * x - y) * z**2

def generateTable(x, y, z, xMean, yMean, zMean, nx, ny, nz):
    zArr = getnArr(zMean, nz, z)
    yArr = getnArr(yMean, ny, y)
    xArr = getnArr(xMean, nx, x)
    table = np.zeros([nz + 1, ny + 1, nx + 1])
    for i in range(nz + 1):
        for j in range(ny + 1):
            for k in range(nx + 1):
                table[i][j][k] = f(zArr[i], yArr[j], xArr[k])
    return table, yArr, zArr, xArr

def calc(table, x, z, y, nx, ny, nz, xMean, yMean, zMean):
    #print(x)
    #print(y)
    #print(z)
    zobsh = []
    for i in range(nz + 1):
        x_for_y = []
        for j in range(ny + 1):
            trgl = getDivededDiff(x, table[i][j], nx + 1)[0, :]
            yzn = getNewtonPoly(trgl, x, xMean, nx + 1)
            x_for_y.append(yzn)
        print(x_for_y)
        trgl = getDivededDiff(y, x_for_y, ny + 1)[0, :]
        zRes = getNewtonPoly(trgl, y, yMean, ny + 1)
        zobsh.append(zRes)
    print(zobsh)
    trgl = getDivededDiff(z, zobsh, nz + 1)[0, :]
    res = getNewtonPoly(trgl, z, zMean, nz + 1)
    return res

nx, ny, nz = get_polynomial_degree()
xMean, yMean, zMean = map(float, input("Input x, y, z: ").split())
x = np.linspace(-5, 5, 20)
y = np.linspace(-3, 4, 50)
z = np.linspace(-1, 2, 30)
table, yArr, zArr, xArr = generateTable(x, y, z, xMean, yMean, zMean, nx, ny, nz)
print("Result: ", calc(table, xArr, zArr, yArr, nx, ny, nz, xMean, yMean, zMean))
#0.37
#0.262 0.131 0.5