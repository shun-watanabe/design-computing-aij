import bezier
import csv  # bezier.pyおよびモジュールcsvの読み込み
import numpy as np  # モジュールnumpyをnpという名前で読み込み
import scipy as sp  # モジュールscipyをspという名前で読み込み
from scipy import optimize  # scipy内のoptimizeモジュールを読み込み
from scipy import integrate  # scipy内のintegrateモジュールを読み込み


filename = 'input1'  # 制御点座標情報を格納した入力ファイル名
reader = csv.reader(open(filename + '.csv', 'r'))  # 入力ファイルの読み込み
next(reader)  # 先頭行は読み飛ばし
row = next(reader)[0:2]
nu, nv = int(row[0]), int(row[1])  # u,v方向の制御点数
next(reader)  # 1行読み飛ばし
cp = []
for row in reader:
    cp.append([float(row[0]), float(row[1]), float(row[2])])  # 制御点座標読み込み
cp = np.array(cp)
limit = [np.min(cp), np.max(cp), np.min(cp), np.max(cp),
         np.min(cp), np.max(cp)]  # 描画範囲
bezier.plot_shape(nu, nv, cp, limit)


def f(x):  # 目的関数の定義
    global cp, nu, nv
    cp[:, 2] = x[:]  # 制御点座標の更新
    return integrate.nquad(lambda u, v: bezier.EGF(nu, nv, u, v, cp), [[0, 1], [0, 1]],
                           opts={'epsabs': 1.0e-6, 'epsrel': 1.0e-6})[0]  # 数値積分


k = 0
b = []  # 設計変数の範囲の設定

for i in range(nu):
    for j in range(nv):
        if i == 0 or i == nu - 1 or j == 0 or j == nv - 1:
            b.append([cp[k, 2], cp[k, 2]])  # 境界は動かさない
        else:
            b.append([-1.0e+10, 1.0e+10])
        k += 1

x = cp[:, 2]
optimize.fmin_slsqp(f, x, fprime=None, bounds=b,
                    iprint=2, full_output=True)  # 逐次二次計画法
bezier.plot_shape(nu, nv, cp, limit)  # 結果の描画
