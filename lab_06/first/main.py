from matplotlib import pyplot as plt
from numpy import linspace, arange
from prettytable import PrettyTable
from gauss import *
from function import *

N_MAX = 12
M_MAX = 12

x_left = 0
x_right = 2
y_bottom = -1
y_top = 1
table = PrettyTable(['Кол-во узлов'] + list(range(2, M_MAX)))
for n in range(2, N_MAX):
    string = [n]
    for m in range(2, M_MAX):
        string.append(f'{gauss_integ(n, m, x_left, x_right, y_bottom, y_top, f):f}')
    table.add_row(string)
print(table)
