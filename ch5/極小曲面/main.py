import bezier,csv
import numpy as np
import scipy as sp
from scipy import optimize
from scipy import integrate
filename='input1'
reader = csv.reader(open(filename+'.csv', 'rb'))
next(reader)
row=next(reader)[0:2]
nu,nv=int(row[0]),int(row[1])
next(reader)
cp=[]
for row in reader:
	cp.append([float(row[0]),float(row[1]),float(row[2])])
cp=np.array(cp)
limit=[np.min(cp),np.max(cp),np.min(cp),np.max(cp),np.min(cp),np.max(cp)]
bezier.plot_shape(nu,nv,cp,limit)
def f(x):
	global cp,nu,nv
	cp[:,2]=x[:]
	return integrate.nquad(lambda u,v: bezier.EGF(nu,nv,u,v,cp), [[0,1],[0,1]],opts={'limlst':3,'limit':1,'epsabs':1.0e-9,'epsrel':1.0e-9})[0]
k=0
b=[]
for i in range(nu):
	for j in range(nv):
		if i==0 or i==nu-1 or j==0 or j==nv-1:
			b.append([cp[k,2],cp[k,2]])
		else:
			b.append([-1.0e+10,1.0e+10])
		k+=1
x=cp[:,2]
optimize.fmin_slsqp(f,x,fprime=None,bounds=b,iprint=2,full_output=True)
bezier.plot_shape(nu,nv,cp,limit)