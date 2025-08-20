import os
import sys
from pymol import cmd

def add_hydrogens_to_sdf(sdf_path, output_dir):
    if not os.path.exists(sdf_path):
        print(f"Error: {sdf_path} not found.")
        return

    # Prepare output filename in sdf_final
    base_name = os.path.basename(sdf_path)
    base, ext = os.path.splitext(base_name)
    output_path = os.path.join(output_dir, f"{base}_H{ext}")

    if os.path.exists(output_path):
        print(f"Output file {output_path} already exists. Skipping.")
        return

    # Reinitialize PyMOL
    cmd.reinitialize()

    # Load input sdf
    cmd.load(sdf_path, "ligand")

    # Add hydrogens
    cmd.h_add("ligand")

    # Save output sdf
    cmd.save(output_path, "ligand", 0)

    # Cleanup
    cmd.reinitialize()

    print(f"✔ Processed {sdf_path} → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_sdf_file_or_directory>")
        sys.exit(1)

    input_path = sys.argv[1]

    # Handle directory vs single file
    if os.path.isdir(input_path):
        # Make sdf_final directory at the same level as input_path
        parent_dir = os.path.dirname(os.path.abspath(input_path))
        output_dir = os.path.join(parent_dir, "sdf_final")
        os.makedirs(output_dir, exist_ok=True)

        # Process all sdf files in directory
        sdf_files = [f for f in os.listdir(input_path) if f.endswith(".sdf")]
        if not sdf_files:
            print(f"No .sdf files found in directory {input_path}")
            sys.exit(0)

        for sdf in sdf_files:
            sdf_full_path = os.path.join(input_path, sdf)
            add_hydrogens_to_sdf(sdf_full_path, output_dir)

    elif os.path.isfile(input_path) and input_path.endswith(".sdf"):
        # If a single file is provided, create sdf_final next to its directory
        parent_dir = os.path.dirname(os.path.abspath(input_path))
        output_dir = os.path.join(parent_dir, "sdf_final")
        os.makedirs(output_dir, exist_ok=True)

        add_hydrogens_to_sdf(input_path, output_dir)

    else:
        print(f"Invalid input: {input_path} (must be .sdf file or directory)")
