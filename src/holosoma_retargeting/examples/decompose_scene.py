import coacd
import trimesh
import numpy as np
import os

input_file = "demo_data/scene/sequence_07/box_models/meshes_all.obj"
output_folder = "demo_data/scene/sequence_07/scene_decomposed"

os.makedirs(output_folder, exist_ok=True)
for f in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, f))


mesh = trimesh.load(input_file, force="mesh")
mesh = coacd.Mesh(mesh.vertices, mesh.faces)
parts = coacd.run_coacd(mesh) # a list of convex hulls.
print(f"Decomposed into {len(parts)} parts.")

# vs_all = []
# fs_all = []

for i, part_mesh in enumerate(parts):
    vs, fs = part_mesh
    part_trimesh = trimesh.Trimesh(vertices=vs, faces=fs)
    output_path = os.path.join(output_folder, f"part_{i:03d}.obj")
    part_trimesh.export(output_path)
    
#     vs_all.append(vs)
#     fs_all.append(fs + sum(len(v) for v in vs_all[:-1]))

# # Save combined mesh as well
# combined_mesh = trimesh.Trimesh(vertices=np.vstack(vs_all), faces=np.vstack(fs_all))
# combined_output_path = os.path.join(output_folder, "multi_boxes.obj")
# combined_mesh.export(combined_output_path)
    
