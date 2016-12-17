from graphillion import GraphSet
import graphillion.tutorial as tl

universe = tl.grid(2, 2)
GraphSet.set_universe(universe)
lines = GraphSet({'include': [(8, 9), (5, 8), (4, 5)], 'exclude': [(6, 9)]})
trees = GraphSet.trees(is_spanning=True)
common = trees & lines

for path in common:
    tl.draw(path)
