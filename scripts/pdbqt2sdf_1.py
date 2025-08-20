import os
import glob
from openbabel import pybel
import argparse

def pdbqt_to_sdf_with_heading_and_hydrogens(pdbqt_file, output_dir):
    mols = list(pybel.readfile('pdbqt', pdbqt_file))
    if not mols:
        print(f"Warning: No molecules found in {pdbqt_file}. Skipping file.")
        return

    # Extract free energy
    free_energy = None
    with open(pdbqt_file, 'r') as pdbqt_f:
        for line in pdbqt_f:
            if line.startswith("REMARK Estimated Free Energy of Binding"):
                free_energy = line.split('=')[1].strip()
    if not free_energy:
        print(f"Warning: Missing Estimated Free Energy in {pdbqt_file}. Skipping file.")
        return

    root_name = os.path.splitext(os.path.basename(pdbqt_file))[0]

    for idx, mol in enumerate(mols, start=1):
        mol.OBMol.AddHydrogens()
        mol.OBMol.PerceiveBondOrders()
        mol.OBMol.SetTitle(root_name)
        if not mol.OBMol.Has3D():
            mol.make3D()

        if len(mols) == 1:
            output_sdf_file = os.path.join(output_dir, f"{root_name}.sdf")
        else:
            output_sdf_file = os.path.join(output_dir, f"{root_name}_conformer{idx}.sdf")

        temp_sdf_file = output_sdf_file + ".tmp"
        mol.write("sdf", temp_sdf_file, overwrite=True)

        with open(temp_sdf_file, "r") as f:
            lines = f.readlines()

        lines = [l for l in lines if l.strip() != "$$$$"]

        torpedo_start = torpedo_end = None
        for i, line in enumerate(lines):
            if "<TORSDO>" in line:
                torpedo_start = i
            if torpedo_start is not None and line.strip() == "F 4":
                torpedo_end = i + 1
                break
        if torpedo_start is not None and torpedo_end is not None:
            del lines[torpedo_start:torpedo_end]

        lines.append("> <Estimated Free Energy of Binding>\n")
        lines.append(f"{free_energy}\n\n")
        lines.append("$$$$\n")

        with open(output_sdf_file, "w") as f:
            f.writelines(lines)

        os.remove(temp_sdf_file)
        print(f"Saved {output_sdf_file}")


def process_pdbqt_path(pdbqt_path):
    # Expand path (handles both dirs and glob patterns)
    if os.path.isdir(pdbqt_path):
        pdbqt_files = glob.glob(os.path.join(pdbqt_path, "*.pdbqt"))
    else:
        pdbqt_files = glob.glob(pdbqt_path)

    if not pdbqt_files:
        print(f"No .pdbqt files found for: {pdbqt_path}")
        return

    # Create sibling sdf_output directory
    base_dir = os.path.dirname(pdbqt_files[0])  # where pdbqt files live
    parent_dir = os.path.dirname(base_dir)
    output_dir = os.path.join(parent_dir, "sdf_intermediate")
    os.makedirs(output_dir, exist_ok=True)

    for pdbqt_file in pdbqt_files:
        pdbqt_to_sdf_with_heading_and_hydrogens(pdbqt_file, output_dir)


def parse_args():
    parser = argparse.ArgumentParser(description="Convert PDBQT to SDF")
    parser.add_argument("pdbqt_path", type=str, help="Directory containing PDBQT files or a glob pattern (*.pdbqt)")
    return parser.parse_args()


def main():
    args = parse_args()
    process_pdbqt_path(args.pdbqt_path)


if __name__ == "__main__":
    main()
