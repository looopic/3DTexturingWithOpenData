import bpy
import os
import sys

def parse_args():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        print("Usage: blender -P your_script.py -- <model_file> <kml_file>")
        sys.exit(1)
    return args

model, kml = parse_args()

working_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_dir)

# Start Blender
bpy.ops.wm.collada_import(filepath=os.path.join("swissBUILDINGS3D", kml, "models", model))

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

# Combine all selected objects into one
bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
bpy.ops.object.join()

# Get the merged mesh
merged_obj = bpy.context.selected_objects[0]

# Get the Z coordinate of the lowest point of the walls
lowest_z = min([v.co.z for v in merged_obj.data.vertices])

# Select vertices belonging to the floor
bpy.context.view_layer.objects.active = merged_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

for vert in merged_obj.data.vertices:
    if vert.co.z <= lowest_z:
        vert.select = True

# Invert selection to exclude the floor from UV unwrapping
bpy.ops.mesh.select_all(action='INVERT')

# Unwrap UV for the merged mesh
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.objects.active = merged_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')

image = bpy.data.images.load(filepath=os.path.join(working_dir, "texture.png"))
material = bpy.data.materials.new(name="Texture")

material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = image

material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
if merged_obj.data.materials:
    merged_obj.data.materials[0] = material

merged_obj.data.materials.append(material)

# Export the Collada-File
collada_filepath = os.path.join(working_dir, "texturized_model.dae")
bpy.ops.wm.collada_export(filepath=collada_filepath)

# Quit Blender
bpy.ops.wm.quit_blender()
