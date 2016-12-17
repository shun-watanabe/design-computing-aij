import numpy as np
import csv
import matplotlib.pyplot as plt
reader = csv.reader(open('out2.csv', 'rb'))
f_history = []
x1_history = []
x2_history = []
for row in reader:
    break
for row in reader:
    f_history.append(float(row[1]))
    x1_history.append(float(row[2]))
    x2_history.append(float(row[3]))
plt.figure(figsize=(15, 8))
x1 = np.arange(-0.5, 4.5, 0.1)
x2 = np.arange(-0.5, 4.5, 0.1)
X1, X2 = np.meshgrid(x1, x2)
f = np.vectorize(lambda x1, x2: ((2.0 - x1)**2 + (4.0 - x2)**2)
                 ** 0.5 + ((3.0 - x1)**2 + (2.0 - x2)**2)**0.5)
plt.subplot(1, 2, 1)
plt.xlabel('x1')
plt.ylabel('x2')
C = plt.contour(X1, X2, f(X1, X2), 20, colors='black')
plt.clabel(C, inline=1, fontsize=10)
plt.plot(x1_history, x2_history)

zero1 = [0.0] * len(x1)
zero2 = [0.0] * len(x2)
two1 = [2.0] * len(x1)
two2 = [2.0] * len(x2)
h = (-2.0 * x1 + 7.0) / 3.0
plt.plot(x1, zero1, '-', color='gray', label=r'$x_1=0$')
plt.plot(zero2, x2, '--', color='gray', label=r'$x_2=0$')
plt.plot(x1, two1, '-.', color='gray', label=r'$x_1-2=0$')
plt.plot(two2, x2, ':', color='gray', label=r'$x_2-2=0$')
plt.plot(x1, h, '.', color='gray', label=r'$2x_1+3x_2-7=0$')
plt.fill([0, 2, 2, 0.5, 0], [0, 0, 1, 2, 2], alpha=0.1)
plt.legend()

plt.subplot(1, 2, 2)
plt.xlabel('step')
plt.ylabel('f(x)')
plt.plot(f_history)
plt.show()
