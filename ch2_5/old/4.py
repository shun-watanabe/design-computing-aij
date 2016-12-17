import bpy

for i in range(5):
    for j in range(5):
        for k in range(5):
            bpy.ops.mesh.primitive_cube_add(radius = 1, location = (i*5, j*5, k*5))