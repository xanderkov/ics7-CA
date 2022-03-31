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
	slau = []
	column = []

	for k in range(n + 1):
		tmp = 0
		slau.append([0 for m in range(n + 1)])
		for i in range(len(x)):
			tmp += ro[i] * y[i] * phi(x[i], k)
			for j in range(n + 1):
				tmpCoeff = ro[i] * phi(x[i], k + j)
				slau[k][j] += tmpCoeff
		column.append(tmp)

	return slau, column

def getReverseSLAU(slau):
	sz = len(slau)
	res = []

	for i in range(sz):
		res.append([])
		for j in range(sz):
			if (i == j):
				res[i].append(1.0)
			else:
				res[i].append(0.0)

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
	res = []

	for i in range(sz):
		res.append(0)
		for j in range(sz):
			res[i] += slau[i][j] * column[j]

	return res

def graphic(x, y, ro, x_graf, y_graf):
	fig = plt.figure()
	plt.scatter(x, y, label = "исходная таблица", color = "blue")
	plt.plot(x_graf, y_graf, color = "green")
	plt.grid(True)
	plt.legend()
	plt.show()


def main():
    x, y, ro = loadTableXY()
    # n = 2

    n = int(input("Введите степень полинома: "))
    while (n <= 0):
        print("Степень полинома должна быть больше 0\n")
        n = int(input("Введите степень полинома: "))

    slau, column = getCoeffSLAU(x, y, ro, n)
    print(slau, column)
    slau = getReverseSLAU(slau)
    a = multiplication(slau, column)

    print(a)

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

    graphic(x, y, ro, x_graf, y_graf)

if (__name__ == "__main__"):
	main()