# Usage: blender --engine CYCLES --background -P renderer.py -- <object-path>

import os
import sys
import bpy
import re

BASE_DIR = os.getcwd()

RENDER_DIR = os.path.join(BASE_DIR, "render") 

if not os.path.exists(RENDER_DIR):
    os.makedirs(RENDER_DIR)

# Opening materials.blend to get material names

bpy.ops.wm.open_mainfile(filepath=os.path.join(BASE_DIR, 'materials.blend'), load_ui=False)

material_names = bpy.data.materials.keys()

# Open init file

bpy.ops.wm.open_mainfile(filepath=os.path.join(BASE_DIR, 'init.blend'))

# get context and current scene

context = bpy.context
scene = context.scene

# Load desired object

obj_path = os.path.join(BASE_DIR, sys.argv[-1])

bpy.ops.import_scene.obj(filepath=obj_path)

imported_obj = bpy.context.selected_objects[0]

# Materials

# Linking materials from 'materials.blend'

# This 'init.blend' file should have no materials because 
# they would be used to render the objects and this is 
# not the desired behavior. 
# What we want is to use the materials from the 'materials.blend' file

for name in material_names:

    bpy.ops.wm.link(filename=name, directory=os.path.join(os.getcwd(), 'materials.blend', 'Material'))

# get cameras on scene

cameras = []

for obj in bpy.data.objects:
    if (obj.type =='CAMERA'):
        cameras.append(obj)

# The actual rendering routine
# it will render 10 perspectives for every object with every material found

for mat in bpy.data.materials.values():
    imported_obj.data.materials.append(mat)
    imported_obj.data.materials[0] = mat

    for i, cam in enumerate(cameras):
        scene.camera = cam
        bpy.context.scene.render.filepath = os.path.join(RENDER_DIR,
         '%s-%s-%s.png' % (imported_obj.name, mat.name, i))
        bpy.ops.render.render(write_still=True)

