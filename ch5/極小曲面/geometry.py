# -*- coding: utf-8 -*-
# Coded by Shinnosuke Fujita @ KSE 2015.12
#-----------------------------------------------------
# 3次元梁要素のマトリクス演算モジュール
#-----------------------------------------------------
import csv, math, bezier
import numpy as np

global ini_r,ini_area,area,ini_cp

#---------------------------------------------------------------------------------
# [openfile]
# 入力ファイルの読み込み
#---------------------------------------------------------------------------------
def openfile(fname):
	global r,nod,nu,nv,cp,uv,divu,divv
        reader = csv.reader(open(fname, 'rb'))
	cp = []#制御点座標
	u = []#パラメータ
	v = []#パラメータ
	uv = []#[u,v]
	r = []#出力点座標
	
	#ベジエ曲面情報の読み込み
	for row in reader:
		break#先頭行は読み飛ばし
	for row in reader:
		if row[0]=='': break
		nu,nv,divu,divv=int(row[0]),int(row[1]),int(row[2]),int(row[3])
	
	#制御点の読み込み
	for row in reader:
		break#先頭行は読み飛ばし
	for row in reader:
		if row[0]=='': break
		cp.append([float(row[0]),float(row[1]),float(row[2])])
	
	#パラメータの生成(等分割)
	for i in range(nu+(divu-1)*(nu-1)):
		u.append(i*1.0/float(nu+(divu-1)*(nu-1)-1))
	for i in range(nv+(divv-1)*(nv-1)):
		v.append(i*1.0/float(nv+(divv-1)*(nv-1)-1))
	for i in range(len(u)):
		for j in range(len(v)):
			uv.append([u[i],v[j]])
	uv = np.array(uv)
	cp = np.array(cp)
	
	#ベジエ曲面の生成
	r = bezier.bezierplot(nu,nv,uv,cp)
	r = np.array(r)
	nod=len(r)#節点数


#----------------------------------------------------------------
#[EGF]
#[u,v]における微小要素の曲面の面積を求める
#----------------------------------------------------------------
def EGF(nu,nv,u,v,cp):
	z1=np.array([0.0,0.0,0.0])
	z2=np.array([0.0,0.0,0.0])
	for i in range(1,nu+1,1):
		bu=bezier.bernstein(u,nu,i)
		dbu=bezier.d_bern(u,nu,i)
		for j in range(1,nv+1,1):
			bv=bezier.bernstein(v,nv,j)
			dbv=bezier.d_bern(v,nv,j)
			z1[0]=z1[0]+ cp[j-1+(i-1)*nu,0] * dbu * bv
			z2[0]=z2[0]+ cp[j-1+(i-1)*nu,0] * bu * dbv
			z1[1]=z1[1]+ cp[j-1+(i-1)*nu,1] * dbu * bv
			z2[1]=z2[1]+ cp[j-1+(i-1)*nu,1] * bu * dbv
			z1[2]=z1[2]+ cp[j-1+(i-1)*nu,2] * dbu * bv
			z2[2]=z2[2]+ cp[j-1+(i-1)*nu,2] * bu * dbv
	E = z1.dot(z1)
	G = z2.dot(z2)
	F = z1.dot(z2)
	return math.sqrt(abs(E*G-F**2))