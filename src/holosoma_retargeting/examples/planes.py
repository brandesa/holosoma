import os
import glob

def add_thickness_to_obj(file_path, thickness=1.0):
    """
    Reads an OBJ file, extrudes the geometry to add thickness (creating a volume),
    and overwrites the file.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    vertices = []
    faces = []
    header_lines = [] # To keep materials/groups
    
    # 1. Parse the existing file
    for line in lines:
        if line.startswith('v '):
            parts = line.strip().split()
            # Parse x, y, z
            v = [float(parts[1]), float(parts[2]), float(parts[3])]
            vertices.append(v)
        elif line.startswith('f '):
            parts = line.strip().split()
            # Store just the vertex index (ignoring texture/normals like 1/1/1)
            face_indices = []
            for p in parts[1:]:
                idx = int(p.split('/')[0])
                face_indices.append(idx)
            faces.append(face_indices)
        else:
            # Keep other lines (mtllib, usemtl, g, empty lines)
            header_lines.append(line)

    if not vertices or not faces:
        print(f"Skipping empty or invalid file: {file_path}")
        return

    # 2. Generate new vertices (extruded)
    # We shift slightly in X (or Z) to create volume. 
    # Based on your previous manual fix, you shifted X.
    new_vertices = []
    for v in vertices:
        # Shift X by thickness to create the "back" of the wall
        new_v = [v[0] + thickness, v[1], v[2]]
        new_vertices.append(new_v)

    # 3. Write the fixed data back to the file
    with open(file_path, 'w') as f:
        # Write headers (materials, etc)
        for line in header_lines:
            # Simple heuristic: write all headers at top to ensure validity
            if line.strip(): 
                f.write(line)
        
        f.write(f"\n# --- Extrusion Script Generated ---\n")
        f.write(f"# Original Vertices\n")
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            
        f.write(f"\n# Extruded Vertices\n")
        for v in new_vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        f.write(f"\n# Front Faces\n")
        for face in faces:
            f_str = " ".join(str(idx) for idx in face)
            f.write(f"f {f_str}\n")
            
        f.write(f"\n# Back Faces (Reversed)\n")
        num_v = len(vertices)
        for face in faces:
            # Reverse order for correct normal winding on back
            reversed_face = face[::-1]
            # Offset indices by number of original vertices
            new_face_indices = [idx + num_v for idx in reversed_face]
            f_str = " ".join(str(idx) for idx in new_face_indices)
            f.write(f"f {f_str}\n")

        f.write(f"\n# Side Faces (Connecting edges)\n")
        for face in faces:
             for k in range(len(face)):
                v_curr = face[k]
                v_next = face[(k + 1) % len(face)]
                
                # Create a quad connecting the front edge to the back edge
                p1 = v_curr
                p2 = v_next
                p3 = v_next + num_v
                p4 = v_curr + num_v
                
                f.write(f"f {p1} {p2} {p3} {p4}\n")

    print(f"Fixed: {file_path}")

def main():
    # Process all .obj files in the current directory
    target_dir = "demo_data/scene/sequence_07/planes"
    search_path = os.path.join(target_dir, "*.obj")
    files = glob.glob(search_path)
    if not files:
        print("No .obj files found in this directory.")
        return

    print(f"Found {len(files)} files. Applying thickness fix...")
    
    for file_path in files:
        try:
            add_thickness_to_obj(file_path)
        except Exception as e:
            print(f"Error on {file_path}: {e}")

    print("All done! MuJoCo should accept these meshes now.")

if __name__ == "__main__":
    main()