from math import sqrt
from operator import itemgetter


def kdtree(points, axis):
    if not points:
          return None

    median = len(points) // 2
    points.sort(key=itemgetter(axis))
    axis = (axis + 1) % 2

    return [points[median],
               kdtree(points[0:median], axis),
               kdtree(points[median + 1:], axis)]


def nnsearch(node, query, max_sqd, axis):
    if node is None:
          return(node, float("inf"))

    point = node[0]
    if query[axis] < point[axis]:
          nearer = node[1]
          further = node[2]
    else:
          nearer = node[2]
          further = node[1]

    n1 = nnsearch(nearer, query, max_sqd, (axis + 1) % 2)
    nearest = n1[0]
    sqd = n1[1]

    if sqd < max_sqd:
          max_sqd = sqd
    d = (point[axis] - query[axis]) ** 2
    if d > max_sqd:
          return(nearest, sqd)
    d = (point[0] - query[0])**2 + (point[1] - query[1])**2
    if d < sqd:
          nearest = point
          sqd = d
          max_sqd = sqd

    n2 = nnsearch(further, query, max_sqd, (axis + 1) % 2)
    if n2[1] < sqd:
          nearest = n2[0]
          sqd = n2[1]

    return(nearest, sqd)

point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
tree = kdtree(point_list, 0)
n = nnsearch(tree, (9, 2), float("inf"), 0)
print('nearest:', n[0], 'dist:', sqrt(n[1]))
# nearest: (8, 1) dist: 1.4142135623730951