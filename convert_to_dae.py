import bpy
import os
import sys

def parse_args():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        print("Usage: blender -P your_script.py -- <model_file> <kml_file>")
        sys.exit(1)
    return args

def conversion(input_file, output_file):
    # Load the model blend file
    bpy.ops.wm.open_mainfile(filepath=input_file)

    #Select the object in the scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = bpy.context.scene.objects[1]
    bpy.context.scene.objects.active.select = True

    # Export the model to Collada format
    bpy.ops.wm.collada_export(filepath=output_file, selected=True, check_existing=False, export_selected=True, include_children=True, use_uv_map=True)

    # Quit Blender
    bpy.ops.wm.quit_blender()

model, kml = parse_args()

# Working directory
working_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_dir)

collada_file = os.path.join("swissBUILDINGS3D", kml, "models", model)
file_name = os.path.splitext(os.path.basename(collada_file))[0]

input_file = os.path.join(working_dir, os.path.dirname(collada_file), file_name + "_texturated.blend")
output_file = os.path.join(working_dir, os.path.dirname(collada_file), file_name + "_texturated.dae")

# Perform conversion
conversion(input_file, output_file)
