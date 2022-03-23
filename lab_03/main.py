
import numpy as np
import Newton
import pandas as pd
import matplotlib.pyplot as plt


def make_table(N=11):
    data = pd.read_csv("points.csv")
    data.head(data.size)
    print(data)
    return {'x' : data['x'].values, 'y' : data['y'].values}

def countCoefSplain(data, N):
    data['h'] = [None] + list(data['x'][i] - data['x'][i - 1]
                            for i in range(1, N))

    data['f'] = [None, None] + list(3 * (((data['y'][i] - data['y'][i - 1]) / data['h'][i]) -
                                    ((data['y'][i - 1] - data['y'][i - 2]) / data['h'][i - 1]))
                                    for i in range(2, N))
    data['xi'] = [None, None] + [0]
    for i in range(3, N + 1):
        xi_i = -data['h'][i - 1] / (data['h'][i - 2] * data['xi'][i - 1] +
                        2 * (data['h'][i - 2] + data['h'][i - 1]))
        data['xi'].append(xi_i)

    data['eta'] = [None, None] + [0]
    for i in range(3, N + 1):
        eta_i = ((data['f'][i - 1] - data['h'][i - 2] * data['eta'][i - 1]) /
                (data['h'][i - 2] * data['xi'][i - 1] + 2 * (data['h'][i - 2] + data['h'][i - 1])))
        data['eta'].append(eta_i)

    # обратные ход: при условии c[N+1]=0, определяем все коэффициенты c
    # с помощью прогоночных коэффициентов
    data['c'] = [None] + [0] * (N)
    for i in range(N - 1, 0, -1):
        data['c'][i] = data['xi'][i + 1] * data['c'][i + 1] + data['eta'][i + 1]

    # с помощью коэффициентов c находим коэффициенты b и d
    data['b'] = [None] + list((data['y'][i] - data['y'][i - 1]) / data['h'][i] -
                            data['h'][i] * (data['c'][i + 1] - 2 * data['c'][i]) / 3
                            for i in range(1, N))

    data['d'] = [None] + list((data['c'][i + 1] - data['c'][i]) / 3 / data['h'][i]
                            for i in range(1, N))

    # находим все коэффициенты a из условия, что в узлах значения многочлена и интерполируемой функции совпадают
    data['a'] = [None] + list(data['y'][i - 1] for i in range(1, N))
    return data

# поиск коэффициентов полинома на участке, в котором находится точка x
# а также точки, с которой начинается этот участок
def choose_coeffs(data, x, N):
    i_beg = 0
    for i in range(1, N - 1):
        if x < data['x'][i]:
            i_beg = i
            break
    return [data['a'][i_beg], data['b'][i_beg], data['c'][i_beg], data['d'][i_beg],
            data['x'][i_beg - 1]]

# подсчет значения полинома в точке x на участке, начинающемся с точки x0
def count_polynom3(a, b, c, d, x0, x):    
    return (a + b * (x - x0) + c * (x - x0) ** 2 + d * (x -x0) ** 3)

def makeSpline(data, N, x):
    
    data = countCoefSplain(data, N)
    coeffs = choose_coeffs(data, x, N)
    res_spline = count_polynom3(*coeffs, x)
    return res_spline
 
def main():
    data = make_table()
    N = len(data['x'])
    # вводим значения x и интерполируем кубическим сплайном
    x1 = 0.5
    res_spline1 = makeSpline(data, N, x1)

    x2 = 8.5
    res_spline2 = makeSpline(data, N, x2)
    res_newton1 = Newton.makeNewtonAprox(data['x'], data['y'], 3, x1)
    res_newton2 = Newton.makeNewtonAprox(data['x'], data['y'], 3, x2)

    # вывод и сравнение результатов
    print('Точка:', x1)
    print('Интерполяция кубическим сплайном:', res_spline1)
    print('Интерполяция полиномом Ньютона 3 степени:', res_newton1)
    print()

    print('Точка:', x2)
    print('Интерполяция кубическим сплайном:', res_spline2)
    print('Интерполяция полиномом Ньютона 3 степени:', res_newton2)
    
    xGraph = np.arange(data['x'][0], data['x'][N - 1], 0.01)
    yGraph = np.zeros(xGraph.size)
    for i in range(xGraph.size):
        yGraph[i] = Newton.makeNewtonAprox(data['x'], data['y'], 3, xGraph[i])
    xSpline = np.arange(data['x'][1], data['x'][N - 2], 0.01)
    ySpline = np.zeros(xGraph.size)
    for i in range(xSpline.size):
        ySpline[i] = makeSpline(data, N, xGraph[i])
    plt.plot(xGraph, yGraph)
    plt.plot(xGraph, ySpline)
    plt.plot(data['x'], data['y'], 'bo')
    plt.show()
    
if __name__ == "__main__":
    main()