import bpy
import os
import sys

def join_objects(objects):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()

def unwrap():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

def save_uv_map(file_path):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.export_layout(filepath=file_path, check_existing=False, mode='PNG')
    bpy.ops.object.mode_set(mode='OBJECT')

def save_model_blend(obj, file_path):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.save_mainfile(filepath=file_path)

def process_collada_file(collada_file):
    # Load collada file
    bpy.ops.wm.collada_import(filepath=collada_file)
    # Get all objects in the scene
    objects = bpy.context.scene.objects
    # Filter out objects that are not meshes
    mesh_objects = [obj for obj in objects if obj.type == 'MESH']
    # Join all mesh objects into a single mesh
    join_objects(mesh_objects)
    # Unwrap the joined mesh
    unwrap()
    # Set file path for UV map
    file_name = os.path.splitext(os.path.basename(collada_file))[0]
    file_path = os.path.join(os.path.dirname(collada_file), file_name + "_uv_map.png")
    # Save UV map as PNG
    save_uv_map(file_path)
    print("UV map saved at:", file_path)
    # Set file path for the model with UV map
    model_blend_file_path = os.path.join(os.path.dirname(collada_file), file_name + "_with_uv_map.blend")
    # Save model with UV map as Blender file
    save_model_blend(mesh_objects[0], model_blend_file_path)
    print("Model with UV map saved as blend file at:", model_blend_file_path)
    # Quit Blender
    bpy.ops.wm.quit_blender()

def parse_args():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        print("Usage: blender -P your_script.py -- <model_file> <kml_file>")
        sys.exit(1)
    return args

model, kml = parse_args()

working_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_dir)

collada_file = os.path.join("swissBUILDINGS3D", kml, "models", model)
process_collada_file(collada_file)