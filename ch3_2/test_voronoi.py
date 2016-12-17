import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

np.random.seed(0)  # 再現性のために乱数にシード（種）を与える。
points = np.random.rand(30, 2)

vor = Voronoi(points)
voronoi_plot_2d(vor)
plt.show()
