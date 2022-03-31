from asyncio import run_coroutine_threadsafe
import numpy as np
import Newton
import pandas as pd
import matplotlib.pyplot as plt
import Spline


def make_table(N=11):
    data = pd.read_csv("points.csv")
    data.head(data.size)
    print(data)
    return {'x' : data['x'].values, 'y' : data['y'].values}


def main():
    data = make_table()
    
    N = len(data['x'])
    x = float(input("Enter x: "))
    
    start1 = 0
    end1 = 0
    start2 = Newton.makeNewtonAproxDif2(data['x'], data['y'], 3, data['x'][0])
    end2 = 0
    start3 = Newton.makeNewtonAproxDif2(data['x'], data['y'], 3, data['x'][0])
    end3 = Newton.makeNewtonAproxDif2(data['x'], data['y'], 3, data['x'][-1])
    res_spline1 = Spline.spline(data, x, start1, end1)
    res_spline2 = Spline.spline(data, x, start2, end2)
    res_spline3 = Spline.spline(data, x, start3, end3)
    
    res_newton = Newton.makeNewtonAprox(data['x'], data['y'], 3, x)
    print('Точка:', x)
    print(start2)
    print('Интерполяция кубическим сплайном:', res_spline1)
    print('Интерполяция кубическим сплайном с Ньютоном в левой точке:', res_spline2)
    print('Интерполяция кубическим сплайном с Ньютоном в левой точке и правой точке:', res_spline3)
    print(res_newton)
    xGraph = np.arange(data['x'][0], data['x'][N - 1], 0.01)
    yGraph = np.zeros(xGraph.size)
    for i in range(xGraph.size):
        yGraph[i] = Newton.makeNewtonAprox(data['x'], data['y'], 3, xGraph[i])
    xSpline = np.arange(data['x'][0], data['x'][N - 1], 0.01)
    ySpline = np.zeros(xSpline.size)
    for i in range(xSpline.size):
        ySpline[i] = Spline.spline(data, xSpline[i], start1, end1)
    

    
    plt.plot(xGraph, yGraph)
    plt.plot(xSpline, ySpline)
    plt.plot(data['x'], data['y'], 'bo')
    plt.show()
    
if __name__ == "__main__":
    main()