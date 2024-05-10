import bpy
import os
import sys

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Unsupported type for addition")

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

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

# Create a new material
mat = bpy.data.materials.new(name="MyMaterial")

# Assign the material to the object
if merged_obj.data.materials:
    # If the merged object already has materials, just use the first one
    merged_obj.data.materials[0] = mat
else:
    # Otherwise, append the material
    merged_obj.data.materials.append(mat)

# Ensure the material has a node tree
if mat.node_tree is None:
    mat.use_nodes = True

# Clear existing nodes and create a principled BSDF node
nodes = mat.node_tree.nodes
for node in nodes:
    nodes.remove(node)

principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
output_node = nodes.new(type='ShaderNodeOutputMaterial')
output_node.location = principled_node.location + Vector(300, 0)

# Connect texture node to principled BSDF node
texture_node = nodes.new('ShaderNodeTexImage')
mat.node_tree.links.new(texture_node.outputs[0], principled_node.inputs['Base Color'])

# Load texture image
bpy.ops.image.open(filepath=os.path.join(working_dir, 'Images', 'texture.png'))
texture_image = bpy.data.images["texture.png"]
texture_node.image = texture_image

# Create UV map from the PNG image
uv_map = bpy.data.images.load(os.path.join(working_dir, "uv_map.png"))

# Create UV mapping for the object
bpy.context.view_layer.objects.active = merged_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
bpy.ops.object.mode_set(mode='OBJECT')

# Apply the UV map
merged_obj.data.uv_layers.new(name="UVMap")
uv_layer = merged_obj.data.uv_layers["UVMap"]
uv_layer.active = True
uv_layer.active_render = True

# Export COLLADA model with textures and UV map
bpy.ops.wm.collada_export(filepath=model,
                           selected=True, include_uv_textures=True, include_materials=True)
