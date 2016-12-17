# -*- coding: utf-8 -*-
# Coded by Shinnosuke Fujita @ KSE 2015.7
#-----------------------------------------------------
# グラフ描画モジュール
#-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from mpl_toolkits.mplot3d import proj3d

#-----------------------------------------------------
#描画の手法を透視投影から平行投影に変更する
#-----------------------------------------------------
def orthogonal_transformation(zfront, zback):
	a = 2/(zfront-zback)
	b = -1*(zfront+zback)/(zfront-zback)
	c = zback
	return np.array([[1,0,0,0],
			[0,1,0,0],
			[0,0,a,b],
			[0,0,0,c]])

#-----------------------------------------------------
#グラフの描画
#-----------------------------------------------------
def plot_shape(r,cp,divu,divv,xmin,xmax,ymin,ymax,zmin,zmax):
	proj3d.persp_transformation = orthogonal_transformation
	fig = plt.figure()
	ax = Axes3D(fig)
	x=[]
	y=[]
	z=[]
	k=-1
	for i in range(divu+1):
		xi=[]
		yi=[]
		zi=[]
		for j in range(divv+1):
			k=k+1
			xi.append(r[k,0])
			yi.append(r[k,1])
			zi.append(r[k,2])
		x.append(xi)
		y.append(yi)
		z.append(zi)
	ax.plot_surface(x,y,z, rstride=1, cstride=1)
	ax.plot(cp[:,0],cp[:,1],cp[:,2],'o',color='g',ms=4)
	ax.set_xlim(xmin,xmax)
	ax.set_ylim(ymin,ymax)
	ax.set_zlim(zmin,zmax)
	plt.show()