import bpy
import os
import sys

def assign_texture(obj, texture_image):
    # Create a new material
    mat = bpy.data.materials.new(name="Texture Material")
    mat.use_nodes = True
    
    # Access the Principled BSDF node
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Load the texture image
    tex_image = bpy.data.images.load(texture_image)
    
    # Create a new texture node
    tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_node.image = tex_image
    
    # Link the texture to the base color of the material
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
    
    # Assign the material to the object
    obj.data.materials.clear()
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def parse_args():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        print("Usage: blender -P texturing.py -- <model_file> <kml_file>")
        sys.exit(1)
    return args

def main():
    model, kml = parse_args()

    working_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(working_dir)

    collada_file = os.path.join("swissBUILDINGS3D", kml, "models", model)
    file_name = os.path.splitext(os.path.basename(collada_file))[0]

    # Path to the model blend file with UV map
    model_blend_file = os.path.join(working_dir,os.path.dirname(collada_file), file_name + "_with_uv_map.blend")
    model2_blend_file = os.path.join(working_dir,os.path.dirname(collada_file), file_name + "_texturated.blend")
    
    # Path to the texture image
    texture_image = os.path.join(working_dir,os.path.dirname(collada_file), file_name + "_texture.png")
    
    # Load the model blend file
    bpy.ops.wm.open_mainfile(filepath=model_blend_file)
    
    # Get the object in the scene
    obj = bpy.context.scene.objects[1]
    
    # Assign texture to the model
    assign_texture(obj, texture_image)
    
    # Save the modified blend file
    bpy.ops.wm.save_as_mainfile(filepath=model2_blend_file)

    bpy.ops.wm.quit_blender()

if __name__ == "__main__":
    main()