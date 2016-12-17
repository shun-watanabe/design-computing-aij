import numpy as np  # モジュールnumpyをnpという名前で読み込み
import csv  # モジュールcsvの読み込み
from numba.decorators import jit  # just-in timeコンパイラの読み込み#
import matplotlib.pyplot as plt  # モジュールmatplotlibのpyplot関数を
# pltという名前で読み込み
from mpl_toolkits.mplot3d import Axes3D  # matplotlibの3次元モジュール
from mpl_toolkits.mplot3d import proj3d  # matplotlibの3次元モジュール


@jit
def bernstein(t, n, i):  # bernstein既定関数の定義
    cn, ci, cni = 1.0, 1.0, 1.0
    for k in range(2, n, 1):
        cn = cn * k
    for k in range(1, i, 1):
        if i == 1:
            break
        ci = ci * k
    for k in range(1, n - i + 1, 1):
        if n == i:
            break
        cni = cni * k
    j = t**(i - 1) * (1 - t)**(n - i) * cn / (ci * cni)
    return j


@jit
def d_bern(t, n, i):  # bernstein既定関数の微分の定義
    cn, ci, cni = 1.0, 1.0, 1.0
    for k in range(2, n, 1):
        cn = cn * k
    for k in range(1, i, 1):
        if i == 1:
            break
        ci = ci * k
    for k in range(1, n - i + 1, 1):
        if n == i:
            break
        cni = cni * k
    j = t**(i - 2) * (1 - t)**(n - i - 1) * cn * \
        ((1 - n) * t + i - 1) / (ci * cni)
    return j


def bezierplot(nu, nv, uv, cp):  # bezier曲面の定義
    xyz = np.zeros([len(uv), 3])
    for k in range(len(uv)):
        u, v, sum1, sum2, sum3, l = uv[k, 0], uv[k, 1], 0.0, 0.0, 0.0, 0
        for i in range(1, nu + 1, 1):
            bu = bernstein(u, nu, i)
            for j in range(1, nv + 1, 1):
                bv = bernstein(v, nv, j)
                sum1 += cp[l, 0] * bu * bv
                sum2 += cp[l, 1] * bu * bv
                sum3 += cp[l, 2] * bu * bv
                l += 1
        xyz[k, :] = [sum1, sum2, sum3]
    return np.array(xyz)


@jit
def EGF(nu, nv, u, v, cp):  # bezier曲面の面積を求める関数
    z1, z2, l = np.zeros(3), np.zeros(3), 0
    for i in range(1, nu + 1, 1):
        bu, dbu = bernstein(u, nu, i), d_bern(u, nu, i)
        for j in range(1, nv + 1, 1):
            bv = bernstein(v, nv, j)
            dbv = d_bern(v, nv, j)
            z1[0] += cp[l, 0] * dbu * bv
            z2[0] += cp[l, 0] * bu * dbv
            z1[1] += cp[l, 1] * dbu * bv
            z2[1] += cp[l, 1] * bu * dbv
            z1[2] += cp[l, 2] * dbu * bv
            z2[2] += cp[l, 2] * bu * dbv
            l += 1
    E, G, F = z1.dot(z1), z2.dot(z2), z1.dot(z2)
    return (abs(E * G - F**2))**0.5


def orthogonal_transformation(zfront, zback):  # 曲面の描画を
    a, b, c = 2 / (zfront - zback), -1 * (zfront + zback) / \
        (zfront - zback), zback
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, a, b], [0, 0, 0, c]])


def plot_shape(nu, nv, cp, limit):  # bezier曲面を描画する関数
    proj3d.persp_transformation = orthogonal_transformation
    u, v = np.arange(0, 1 + 0.1, 0.1), np.arange(0, 1 + 0.1, 0.1)  # パラメータ生成
    uv = [[i, j] for i in u for j in v]  # パラメータを格子状に配置
    uv = np.array(uv)  # リストのarray変換
    s = bezierplot(nu, nv, uv, cp)  # bezier曲面生成
    k = 0
    x, y, z = [], [], []
    for i in range(len(u)):  # 生成した節点座標ベクトルを行ごとに分解
        xi, yi, zi = [], [], []
        for j in range(len(v)):
            xi.append(s[k, 0]), yi.append(s[k, 1]), zi.append(s[k, 2])
            k += 1
        x.append(xi), y.append(yi), z.append(zi)
    cx, cy, cz = [], [], []
    k = 0
    for i in range(nu):  # 生成した制御座標ベクトルを行ごとに分解
        cxi, cyi, czi = [], [], []
        for j in range(nv):
            cxi.append(cp[k, 0]), cyi.append(cp[k, 1]), czi.append(cp[k, 2])
            k += 1
        cx.append(cxi), cy.append(cyi), cz.append(czi)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_axis_off(), ax.set_aspect('equal')
    ax.set_xlim(limit[0], limit[1]), ax.set_ylim(limit[2], limit[3]),
    ax.set_zlim(limit[4], limit[5])
    ax.plot_surface(x, y, z, rstride=1, cstride=1)  # bezier曲面の描画
    ax.plot_wireframe(cx, cy, cz, color='g', linestyle='dashed')  # 制御ネット描画
    ax.plot(cp[:, 0], cp[:, 1], cp[:, 2], color='g',
            lw=0, marker='o', ms=5)  # 制御点の描画
    plt.show()
