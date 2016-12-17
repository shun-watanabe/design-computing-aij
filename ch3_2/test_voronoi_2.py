# Voronoi diagram for a set of point:

import numpy as np

# points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
# [2, 0], [2, 1], [2, 2]])

# from __future__ import division, print_function, absolute_import

np.random.seed(0)  # 再現性のために乱数にシード（種）を与える。
points = np.random.rand(30, 2)
points2 = np.random.rand(30, 3)
print(points2)

from scipy.spatial import Voronoi, voronoi_plot_2d
try:
    from scipy._lib.decorator import decorator as _decorator
except:
    from scipy.lib.decorator import decorator as _decorator

vor = Voronoi(points)
vor2 = Voronoi(points2)


@_decorator
def _held_figure(func, obj, ax=None, **kw):
    import matplotlib.pyplot as plt

    if ax is None:
        fig = plt.figure()
        ax = fig.gca()

    was_held = ax.ishold()
    try:
        ax.hold(True)
        return func(obj, ax=ax, **kw)
    finally:
        ax.hold(was_held)


def _adjust_bounds(ax, points):
    ptp_bound = points.ptp(axis=0)
    ax.set_xlim(points[:, 0].min() - 0.1 * ptp_bound[0],
                points[:, 0].max() + 0.1 * ptp_bound[0])
    ax.set_ylim(points[:, 1].min() - 0.1 * ptp_bound[1],
                points[:, 1].max() + 0.1 * ptp_bound[1])


@_held_figure
def voronoi_plot_2d(vor, ax=None, **kw):
    from matplotlib.collections import LineCollection

    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    if kw.get('show_points', True):
        ax.plot(vor.points[:, 0], vor.points[:, 1], '.')
    if kw.get('show_vertices', True):
        ax.plot(vor.vertices[:, 0], vor.vertices[:, 1], 'o')

    line_colors = kw.get('line_colors', 'k')
    line_width = kw.get('line_width', 1.0)
    line_alpha = kw.get('line_alpha', 1.0)

    line_segments = []
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            line_segments.append([(x, y) for x, y in vor.vertices[simplex]])

    lc = LineCollection(line_segments,
                        colors=line_colors,
                        lw=line_width,
                        linestyle='solid')
    lc.set_alpha(line_alpha)
    ax.add_collection(lc)
    ptp_bound = vor.points.ptp(axis=0)

    line_segments = []
    center = vor.points.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            line_segments.append([(vor.vertices[i, 0], vor.vertices[i, 1]),
                                  (far_point[0], far_point[1])])

    lc = LineCollection(line_segments,
                        colors=line_colors,
                        lw=line_width,
                        linestyle='dashed')
    lc.set_alpha(line_alpha)
    ax.add_collection(lc)
    _adjust_bounds(ax, vor.points)

    return ax.figure

# print vor2.ridge_vertices
# print vor2.ridge_points

# Plot it:

import matplotlib.pyplot as plt
voronoi_plot_2d(vor)
plt.show()
