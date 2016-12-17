import numpy as np
import csv
import matplotlib.pyplot as plt
reader = csv.reader(open('out.csv', 'rb'))
f_history=[]
x1_history=[]
x2_history=[]
for row in reader:
    break
for row in reader:
    f_history.append(float(row[1]))
    x1_history.append(float(row[2]))
    x2_history.append(float(row[3]))
plt.figure(figsize=(15,8))
x1=np.arange(1.25, 4.75, 0.1)
x2=np.arange(0.25, 3.75, 0.1)
X1,X2=np.meshgrid(x1,x2)
f=np.vectorize(lambda x1,x2: 0.50*(x1-3.0)**2+(x2-2.0)**2)
plt.subplot(1,2,1)
plt.xlabel('x1')
plt.ylabel('x2')
C=plt.contour(X1,X2,f(X1,X2),20,colors='black')
plt.clabel(C, inline=1, fontsize=10)
plt.plot(x1_history,x2_history)
plt.subplot(1,2,2)
plt.xlabel('step')
plt.ylabel('f(x)')
plt.plot(f_history)
plt.show()
