from math import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

def phi(x, k):
	return pow(x, k)

def loadTableXY():
    data = pd.read_csv("points.csv")
    data.head(data.size)
    print(data)
    x = data['x'].values
    y = data['y'].values
    ro = data["ro"].values
    N = len(x)
    return x, y, ro, N

def create_table(N):
    f = open("ranompoints.txt", "w")
    ymax = 6
    ymin = -5
    y0 = 0
    xarr = np.zeros(N)
    yarr = np.zeros(N)
    ro = np.zeros(N)
    for i in range(N):
        y = y0 + random.random() * (ymax - ymin) + ymin
        y0 = y
        f.write("%d %f %d\n" % (i, y, 1))
        xarr[i] = i
        yarr[i] = y
        ro[i] = 1
    return xarr, yarr, ro
        

def matr_for_gauss(x, y, ro, n, N):
    sum_x = np.zeros(n * 2)
    for i in range(n * 2):
        sum_xi = 0
        for j in range(N):
            sum_xi += phi(x[j], i) * ro[j]
        sum_x[i] = sum_xi
    sum_x_y = np.zeros(n)
    for i in range(n):
        sum_yi = 0
        for j in range(N):
            sum_yi += phi(x[j], i) * ro[j] * y[j]
        sum_x_y[i] = sum_yi

    gmatr = []
    for i in range(n):
        gstr = []
        for j in range(n):
            gstr.append(sum_x[i+j])
        gstr.append(sum_x_y[i])
        gmatr.append(gstr)
    return gmatr

def gauss(gmatr, n):
    for i in range(n):
        for j in range(i+1, n):
            k = -(gmatr[j][i] / gmatr[i][i])
            for l in range(i, n+1):
                gmatr[j][l] += k * gmatr[i][l]
    
    a = np.zeros(n)
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            gmatr[i][n] -= a[j] * gmatr[i][j]
        a[i] = gmatr[i][n] / gmatr[i][i]
    return a


def f(x, a):
    res = []
    for j in range(len(x)):
        rezi = 0
        for i in range(len(a)):
            rezi += a[i]*(x[j]**i)
        res.append(rezi)
    return res


def makeGraph(x, y, a, n):
    
    xGraph = np.arange(x[0], x[len(x) - 1], 0.01)
    yGraph = np.zeros(xGraph.size)
    yGraph = f(xGraph, a)
    
    return xGraph, yGraph

def graphic(x, y, x_graf, y_graf, n):
	fig = plt.figure()
	plt.scatter(x, y, label = "Степень полинома: {}".format(n), color = "blue")
	plt.plot(x_graf, y_graf, color = "green")
	plt.grid(True)
	plt.legend()
	plt.show()


def main():
    N = 6
    x, y, ro, N = loadTableXY()

    n = int(input("Введите степень полинома: "))
    while (n <= 0):
        print("Степень полинома должна быть больше 0\n")
        n = int(input("Введите степень полинома: "))
    gmatr = matr_for_gauss(x, y, ro, n, N)
    a = gauss(gmatr, n)
    xGraph, yGraph = makeGraph(x, y, a, n)
    graphic(x, y, xGraph, yGraph, n)
	

if __name__ == "__main__":
	main()