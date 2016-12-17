# -*- coding: utf-8 -*-
#-----------------------------------------------------
# 最適化モジュール
#-----------------------------------------------------
import numpy as np
import scipy as sp
from scipy import optimize
from scipy import sparse
from scipy import integrate
import threading,math,bezier,graph

def f(x):# 目的関数は曲面の面積
	bezier.cp[:,2]=x[:]
#	bezier.r = bezier.bezierplot(bezier.nu,bezier.nv,bezier.uv,bezier.cp)
	bezier.area = integrate.nquad(lambda u,v: bezier.EGF(bezier.nu,bezier.nv,u,v,bezier.cp), [[0,1],[0,1]],opts={'limlst':3,'limit':1,'epsabs':1.0e-9,'epsrel':1.0e-9})[0]
	return bezier.area

def callbackF(x):# ここで最適化の各ステップでプログラムを動作させることができる
	pass
def opt():
	#-----設計変数の範囲の設定(ここでは4周の制御点を固定,その他は-25～25としている)
	b=np.matrix([[-25.0,25.0]]*bezier.nu*bezier.nv)
	for i in [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]:
		b[i,0],b[i,1]=bezier.ini_cp[i,2],bezier.ini_cp[i,2]
	#-----
	x = bezier.cp[:,2]# 設計変数の初期値(ここでは制御点鉛直方向座標)
	result=optimize.fmin_slsqp(f, x, fprime=None, bounds=b, iprint=2, callback=callbackF, acc=1.0e-9, epsilon=1.0e-9,full_output=True)#制約条件はなし,感度解析は差分による自動計算
	return result