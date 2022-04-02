from math import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def phi(x, k):
	return pow(x, k)

def loadTableXY():
    data = pd.read_csv("points.csv")
    data.head(data.size)
    print(data)
    x = data['x'].values
    y = data['y'].values
    ro = data["ro"].values
    return x, y, ro


def getCoeffSLAU(x, y, ro, n):
	slau = np.zeros([n + 1, n + 1])
	column = np.zeros([n + 1])

	for k in range(n + 1):
		tmp = 0
		for i in range(len(x)):
			tmp += ro[i] * y[i] * phi(x[i], k)
			for j in range(n + 1):
				tmpCoeff = ro[i] * phi(x[i], k + j)
				slau[k][j] += tmpCoeff
		column[k] = tmp

	return slau, column

def getReverseSLAU(slau):
	sz = len(slau)
	res = np.zeros([sz, sz])
	np.diag(np.diag(res, 2))

	for i, j in zip(range(sz), range(sz)):
		if (i == j):
			res[i][j] = 1.0
		else:
			res[i][j] = 0.0

	for i in range(sz):
		for j in range(sz):
			if (i != j):
				tmp = slau[j][i] / slau[i][i]

				for k in range(sz):
					slau[j][k] -= slau[i][k] * tmp
					res[j][k] -= res[i][k] * tmp

	for i in range(sz):
		for j in range(sz):
			res[i][j] /= slau[i][i]

	return res

def multiplication(slau, column):
	sz = len(slau)
	res = np.zeros(sz)

	for i in range(sz):
		for j in range(sz):
			res[i] += slau[i][j] * column[j]

	return res

def makeGraph(x, y, a, n):
    distanceX = x[-1] - x[0] + 1

    stepX = distanceX / 100
    x_graf = []
    y_graf = []

    tmpX = x[0] - stepX * 10

    while (tmpX < x[-1] + stepX * 10):
        x_graf.append(tmpX)
        tmpY = 0
        for k in range(n + 1):
            tmpY += phi(tmpX, k) * a[k]
        y_graf.append(tmpY)
        tmpX += stepX
    
    xGraph = np.arange(x[0], x[len(x) - 1], 0.01)
    yGraph = np.zeros(xGraph.size)
    for i in range(xGraph.size):
        yGraph[i] = phi(xGraph[i], i) * a[i]
    
    return xGraph, yGraph

def graphic(x, y, ro, x_graf, y_graf):
	fig = plt.figure()
	plt.scatter(x, y, label = "исходная таблица", color = "blue")
	plt.plot(x_graf, y_graf, color = "green")
	plt.grid(True)
	plt.legend()
	plt.show()


def main():
    x, y, ro = loadTableXY()

    n = int(input("Введите степень полинома: "))
    while (n <= 0):
        print("Степень полинома должна быть больше 0\n")
        n = int(input("Введите степень полинома: "))

    slau, column = getCoeffSLAU(x, y, ro, n)
    print(slau)
    print(column)
    slau = getReverseSLAU(slau)
    a = multiplication(slau, column)

    print(a)
    x_graf, y_graf = makeGraph(x, y, a, n)
    
    graphic(x, y, ro, x_graf, y_graf)

if __name__ == "__main__":
	main()