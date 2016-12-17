material = bpy.data.materials.new('Red')
material.diffuse_color = (1, 0, 0)
cube.data.materials.append(material)