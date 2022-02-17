import math

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

# df = pd.read_excel('data.xlsx')

# print(df)

import xlrd

file = 'data.xlsx'
xl = pd.ExcelFile(file)
# Print the sheet names
print(xl.sheet_names)
# Load a sheet into a DataFrame by name: df3
df3 = xl.parse('Sheet1')
df3.head(100)
print(df3)

array = [0.464, 0.06, 1.486, 1.022, 1.394, 0.906, 1.179, -1.501, -0.69, 1.372, -0.482, -1.376, -1.01, -0.005, 1.393,
         -1.787, -0.105, -1.339, 1.041, 0.279, -1.805, -1.186, 0.658, -0.439, -1.339, 0.137, -2.526, -0.354, -0.555,
         -0.472, -0.513, -1.055, -0.488, 0.756, 0.225, 1.678, -0.15, 0.598, -0.899, -1.163, -0.261, -0.357, 1.827,
         0.535, -2.056, -2.008, 1.18, -1.141, 0.358, -0.23, 2.455, -0.531, -0.634, 0.046, 1.279, -0.525, 0.007, -0.162,
         -1.618, 0.378, -0.057, 1.356, -0.918, 0.012, -0.911, 1.237, -1.384, -0.959, 0.731, 0.717, -1.633, 1.114, 1.151,
         -1.939, 0.385, -0.068, -0.194, 0.697, 0.321, 3.521, 0.595, 0.769, -0.136, -0.345, 0.761, -1.229, -0.561, 1.598,
         -0.725, 1.231, 1.046, 0.36, 0.424, 1.377, -0.873, 0.542, 0.882, -1.21, 0.891, -0.649]

matplotlib.style.use("ggplot")

# density=True - Распределение частот
# stacked=True- Распредление плотнотсти вероятности
df3["Значение"].plot.hist(density=True, stacked=True)
my_density = stats.gaussian_kde(df3['Значение'])
x = np.linspace(min(df3['Значение']), max(df3['Значение']), 1000)
plt.plot(x, my_density(x), 'g')
print("Оранжевый гистограмма - нормальное распределение")
plt.show()
# print("Синяя гистограмма - нормальное распределение логарифмов")

np.log(df3['Значение']).plot.hist(density=True, stacked=True)
plt.show()

n = 100
C = 0.1
h = 0.8
X = []
for i in range(-23, 34, 8):
    X.append(i / 10)
print(X)
u = []
for i in range(len(X)):
    u.append(round((X[i] - C) / h))
print(u)
intervals = [[-2.7, -1.9], [-1.9, -1.1], [-1.1, -0.3], [-0.3, 0.5], [0.5, 1.3], [1.3, 2.1], [2.1, 2.9], [2.9, 3.7]]
N = []
for i in range(len(intervals)):  # проход по интервалам
    el = 0
    for j in range(len(df3)):  # проход по массиву
        if (df3['Значение'][j] >= intervals[i][0]) & (df3['Значение'][j] < intervals[i][1]):
            el += 1
    N.append(el)
print("N =", N)
# ОЦЕНИВАНИЕ ЧИСЛОВЫХ ХАРАКТЕРИСТИК МЕТОДОМ МОМЕНТОВ ОЦЕНКИ
summ = 0
for i in range(len(N)):
    summ += u[i] ** 1 * N[i]
M1 = 1 / 100 * summ
summ = 0
for i in range(len(N)):
    summ += u[i] ** 2 * N[i]
M2 = 1 / 100 * summ
summ = 0
for i in range(len(N)):
    summ += u[i] ** 3 * N[i]
M3 = 1 / 100 * summ
summ = 0
for i in range(len(N)):
    summ += u[i] ** 4 * N[i]
M4 = 1 / 100 * summ
print("M1 =", M1)
print("M2 =", M2)
print("M3 =", M3)
print("M4 =", M4)

# Находим ЧХ методом моментов оценки
X_B = h * M1 + C
D_B = h ** 2 * (M2 - (M1 ** 2))
SKO_B = D_B ** (1 / 2)
As_B = (h ** 3 * (M3 - 3 * M2 * M1 + 2 * (M1 ** 3))) / (SKO_B ** 3)
Ex_B = (h ** 4 * (M4 - 4 * M3 * M1 + 6 * M2 * (M1 ** 2) - 3 * (M1 ** 4))) / (SKO_B ** 4) - 3
print("")
print("ОЦЕНИВАНИЕ ЧИСЛОВЫХ ХАРАКТЕРИСТИК МЕТОДОМ МОМЕНТОВ ОЦЕНКИ")
print("Мат ожидание =", X_B)
print("Дисперсия =", D_B)
print("СКО =", SKO_B)
print("Асимметрия =", As_B)
print("Эксцесс =", Ex_B)


# ОЦЕНИВАНИЕ ЧИСЛОВЫХ ХАРАКТЕРИСТИК МЕТОД СУММ

def sum_table(X, C, N):
    matrix = []

    for i in range(8):  # проход по строкам
        el = []
        for j in range(4):  # проход по столбцам
            el.append(0)
        matrix.append(el)

    index0 = X.index(C)  # индекс ложного нуля (C = 0.1)

    for j in range(4):  # проход по столбцам
        for i in range(index0):  # проход по строкам до ложного нуля
            if i >= index0 - j:
                continue
            if i == 0:
                matrix[i][j] = N[i]
                continue
            if j == 0:
                matrix[i][j] = matrix[i - 1][j] + N[i]
            else:
                matrix[i][j] = matrix[i - 1][j] + matrix[i][j - 1]

        for i in range(len(X) - 1, index0, -1):  # проход по строкам до ложного нуля (в обратном направлении)
            if i <= index0 + j:
                continue
            if i == len(X) - 1:
                matrix[i][j] = N[i]
                continue
            if j == 0:
                matrix[i][j] = matrix[i + 1][j] + N[i]
            else:
                matrix[i][j] = matrix[i + 1][j] + matrix[i][j - 1]

    return matrix


matrix = sum_table(X, C, N)

b = []
for i in range(len(matrix[0])):
    el = 0
    for j in range(X.index(C)):
        el += matrix[j][i]
    b.append(el)
print(b)

a = []
for i in range(len(matrix[0])):
    el = 0
    for j in range(X.index(C) + 1, len(X)):
        el += matrix[j][i]
    a.append(el)
print(a)

d = []
for i in range(len(a)):
    d.append(a[i] - b[i])
print(d)

s = []
for i in range(len(a)):
    s.append(a[i] + b[i])
print(s)

# Расчёт моментов
M1 = d[0] / n
M2 = (s[0] + 2 * s[1]) / n
M3 = (d[0] + 6 * d[1] + 6 * d[2]) / n
M4 = (s[0] + 14 * s[1] + 36 * s[2] + 24 * s[3]) / n

# Находим ЧХ методом моментов оценки
X_B = h * M1 + C
D_B = h ** 2 * (M2 - (M1 ** 2))
SKO_B = D_B ** (1 / 2)
As_B = (h ** 3 * (M3 - 3 * M2 * M1 + 2 * (M1 ** 3))) / (SKO_B ** 3)
Ex_B = (h ** 4 * (M4 - 4 * M3 * M1 + 6 * M2 * (M1 ** 2) - 3 * (M1 ** 4))) / (SKO_B ** 4) - 3
print("")
print("ОЦЕНИВАНИЕ ЧИСЛОВЫХ ХАРАКТЕРИСТИК МЕТОДОМ СУММ")
print("Мат ожидание =", X_B)
print("Дисперсия =", D_B)
print("СКО =", SKO_B)
print("Асимметрия =", As_B)
print("Эксцесс =", Ex_B)

# НАХОЖДЕНИЕ ДОВЕРИТЕЛЬНЫХ ИНТЕРВАЛОВ
print("")
print("НАХОЖДЕНИЕ ДОВЕРИТЕЛЬНЫХ ИНТЕРВАЛОВ")
ta = 1.984
s = math.sqrt((n / (n - 1)) * D_B)
# print("s =", s)
DI_M_min = abs(X_B) - (ta * s) / (n ** (1 / 2))
DI_M_max = abs(X_B) + (ta * s) / (n ** (1 / 2))
print("Доверительный интервал для среднего")
print(DI_M_min, "<", X_B, "<", DI_M_max)
print("-------------------------------------")

# по таблице функции Лапласа:
z_min = 2.24
z_max = 0.03
x_min = (n - 1) * (1 - (2 / (9 * (n - 1))) + z_min * math.sqrt(2 / (9 * (n - 1)))) ** 3
print("x_min =", x_min)
x_max = (n - 1) * (1 - (2 / (9 * (n - 1))) + z_max * math.sqrt(2 / (9 * (n - 1)))) ** 3
print("x_max =", x_max)
# Эксель:
# x_min = 128.422
# x_max = 73.36108
DI_D_min = (s ** 2 * (n - 1)) / x_min
DI_D_max = (s ** 2 * (n - 1)) / x_max
print("Доверительный интервал для дисперсии")
print(DI_D_min, "<", D_B, "<", DI_D_max)

# ПРОВЕРКА ГИПОТЕЗ
print("")
print("ГИПОТЕЗА 1: о равенстве заданному числу X_B нормально распределённой случайной величины с известной дисперсией")
t_n = (X_B - 0) / ((1 / n) ** (1 / 2))
t_e = 1.984  # по таблице распределения Стьюдента
print(t_n, "<", t_e)

print("ГИПОТЕЗА 2: о равенстве заданному числу D_B нормально распределённой случайной величины")
x_n = (n - 1) * D_B / (1)
z_e = 1.984
x_e = (n - 1) * (1 - (2 / (9 * (n - 1))) + z_e * math.sqrt(2 / (9 * (n - 1)))) ** 3
# x_e = 128.4253
print(x_n, "<", x_e)

# КРИТЕРИИ СОГЛАСИЯ

z = []
for i in range(len(X)):
    z.append(abs((X[i] - X_B) / math.sqrt(D_B)))
print("z =", z)

f = []
for i in range(len(z)):
    f.append(1 / math.sqrt(np.pi * 2 * 1) * np.exp(-0.5 * (z[i] ** 2 - 0)))
print("f =", f)

k = (h * n) / math.sqrt(D_B)
print("k =", k)
kf = []
for i in range(len(f)):
    kf.append(k * f[i])
print("kf =", kf)

xi = 0
i = 0
for i in range(len(N)):
    el = 0
    el += (((N[i] - kf[i]) ** 2) / kf[i])
    xi += el
    print("xi =", el)
print("")
print("Критерий Пирсона =", xi, "<", 6)
print("")
F_1 = []
sum_N = 0
for i in range(len(N)):
    if i < len(N) - 1:
        if i == 0:
            sum_N += N[i]
            F_1.append(N[i])
        sum_N += N[i + 1]
        F_1.append(sum_N)
print("F_1 =", F_1)

F_2 = []
sum_kf = 0
for i in range(len(kf)):
    if i < len(kf) - 1:
        if i == 0:
            sum_kf += kf[i]
            F_2.append(kf[i])
        sum_kf += kf[i + 1]
        F_2.append(sum_kf)
print("F_2 =", F_2)

F_F = []
for i in range(len(N)):
    F_F.append(abs(F_1[i] - F_2[i]))
print("F_F =", F_F)

print("")
print("Критерий Колмогорова-Смирнова =", max(F_F) / len(df3['Значение']), "<", 0.1933)
print("")

# ОЦЕНИВАНИЕ КОЭФФИЦИЕНТА КОРРЕЛЯЦИИ
chet = []  # x
nechet = []  # y
for i in range(len(df3['Значение'])):
    if (i + 1) % 2 == 1:
        nechet.append(df3['Значение'][i])
    else:
        chet.append(df3['Значение'][i])
print("Массив значений с чётными номерами", chet)
print("Массив значений с чётными номерами", nechet)
M = []
for i in range(len(intervals)):
    part = []
    for j in range(len(X)):
        part.append(0)
    M.append(part)

print("")
print("КОРРЕЛЯЦИОННАЯ ТАБЛИЦА")
print("")
for c in range(len(intervals)):
    for r in range(len(intervals)):
        el = 0
        for j in range(int(len(df3) / 2)):
            if (chet[j] >= intervals[c][0]) & (chet[j] < intervals[c][1]) & (nechet[j] >= intervals[r][0]) & (
                    nechet[j] < intervals[r][1]):
                el += 1
        M[c][r] = el
    print(M[c])
print("")
w = []
for i in range(len(M)):
    w.append(sum(M[i]))
print("w =", w)
v = []
for i in range(len(M)):
    summ_x = 0
    for j in range(len(M[i])):
        summ_x += M[j][i]
    v.append(summ_x)
print("v =", v)

nv = []
for i in range(len(M)):
    nv.append(v[i] * u[i])
print("nv =", nv)

nw = []
for i in range(len(M)):
    nw.append(w[i] * u[i])
print("nw =", nw)

nv2 = []
for i in range(len(M)):
    nv2.append(v[i] * (u[i] ** 2))
print("nv2 =", nv2)

nw2 = []
for i in range(len(M)):
    nw2.append(w[i] * (u[i] ** 2))
print("nw2 =", nw2)

res_sum = 0
for j in range(len(M)):
    for i in range(len(M)):
        res_sum += M[i][j] * u[i] * u[j]

v_B = (1 / (n / 2)) * sum(nv)
w_B = (1 / (n / 2)) * sum(nw)
print("v_B =", v_B)
print("w_B =", w_B)

P1 = sum(nv2) - (n / 2) * (v_B ** 2)
P2 = sum(nw2) - (n / 2) * (w_B ** 2)

r_B = (res_sum - (n / 2) * v_B * w_B) / (math.sqrt(P1 * P2))
print("r_B =", r_B)
