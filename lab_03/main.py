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
    data['h'] = [0] + list(data['x'][i] - data['x'][i - 1]
                            for i in range(1, N))

    data['f'] = [0, 0] + list(3 * (((data['y'][i] - data['y'][i - 1]) / data['h'][i]) -
                                    ((data['y'][i - 1] - data['y'][i - 2]) / data['h'][i - 1]))
                                    for i in range(2, N))
    data['xi'] = [0, 0] + [0]
    for i in range(3, N + 1):
        xi_i = -data['h'][i - 1] / (data['h'][i - 2] * data['xi'][i - 1] +
                        2 * (data['h'][i - 2] + data['h'][i - 1]))
        data['xi'].append(xi_i)

    data['eta'] = [0, 0] + [0]
    for i in range(3, N + 1):
        eta_i = ((data['f'][i - 1] - data['h'][i - 2] * data['eta'][i - 1]) /
                (data['h'][i - 2] * data['xi'][i - 1] + 2 * (data['h'][i - 2] + data['h'][i - 1])))
        data['eta'].append(eta_i)


    data['c'] = [0] + [0] * (N)
    for i in range(N - 1, 0, -1):
        data['c'][i] = data['xi'][i + 1] * data['c'][i + 1] + data['eta'][i + 1]


    data['b'] = [0] + list((data['y'][i] - data['y'][i - 1]) / data['h'][i] -
                            data['h'][i] * (data['c'][i + 1] + 2 * data['c'][i]) / 3
                            for i in range(1, N))

    data['d'] = [0] + list((data['c'][i + 1] - data['c'][i]) / 3 / data['h'][i]
                            for i in range(1, N))

    data['a'] = [0] + list(data['y'][i - 1] for i in range(1, N))
    return data


def choose_coeffs(data, x, N):
    i_beg = 0
    for i in range(1, N - 1):
        if x < data['x'][i]:
            i_beg = i
            break
    return [data['a'][i_beg], data['b'][i_beg], data['c'][i_beg], data['d'][i_beg],
            data['x'][i_beg - 1]]

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
    x = float(input("Enter x: "))
    res_spline1 = makeSpline(data, N, x)
    res_newton1 = Newton.makeNewtonAprox(data['x'], data['y'], 3, x)

    print('Точка:', x)
    print('Интерполяция кубическим сплайном:', res_spline1)
    print('Интерполяция полиномом Ньютона 3 степени:', res_newton1)
    
    xGraph = np.arange(data['x'][0], data['x'][N - 1], 0.01)
    yGraph = np.zeros(xGraph.size)
    for i in range(xGraph.size):
        yGraph[i] = Newton.makeNewtonAprox(data['x'], data['y'], 3, xGraph[i])
    xSpline = np.arange(data['x'][0], data['x'][N - 2], 0.01)
    ySpline = np.zeros(xSpline.size)
    for i in range(xSpline.size):
        ySpline[i] = makeSpline(data, N, xGraph[i])
    plt.plot(xGraph, yGraph)
    plt.plot(xSpline, ySpline)
    plt.plot(data['x'], data['y'], 'bo')
    plt.show()
    
if __name__ == "__main__":
    main()