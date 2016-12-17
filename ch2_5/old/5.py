import bpy

nodes=[[0,0,0],
       [1,0,0],
       [1,1,0],
       [0,1,0],
       [0,0,1],
       [1,0,1],
       [1,1,1],
       [0,1,1]]

faces=[[0,1,2,3],
       [4,5,6,7],
       [0,4,5,1],
       [1,2,6,5],
       [3,2,6,7],
       [0,3,7,4]]

mesh_data = bpy.data.meshes.new("cube_mesh_data")
mesh_data.from_pydata(nodes, [], faces)
mesh_data.update()
cube_object = bpy.data.objects.new("cube_object", mesh_data)

scene = bpy.context.scene
scene.objects.link(cube_object)
