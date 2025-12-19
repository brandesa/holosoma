import coacd
import trimesh
import numpy as np

input_file = "demo_data/scene/sequence_07/scene.obj"
mesh = trimesh.load(input_file, force="mesh")
mesh = coacd.Mesh(mesh.vertices, mesh.faces)
parts = coacd.run_coacd(mesh) # a list of convex hulls.
print(f"Decomposed into {len(parts)} parts.")


mesh_parts = []
for vs, fs in parts:
    mesh_parts.append(trimesh.Trimesh(vs, fs))
scene = trimesh.Scene()
np.random.seed(0)
for p in mesh_parts:
    p.visual.vertex_colors[:, :3] = (np.random.rand(3) * 255).astype(np.uint8)
    scene.add_geometry(p)
scene.export("debug_scene.html")
# scene.export(output_file)