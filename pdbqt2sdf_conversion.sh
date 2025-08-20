#!/bin/bash

# Exit on error
set -e

if [ $# -ne 1 ]; then
    echo "Usage: bash shell.sh <path_to_pdbqt_directory>"
    exit 1
fi

PDBQT_DIR=$1

# Resolve absolute path
PDBQT_DIR=$(realpath "$PDBQT_DIR")

# Get parent of the pdbqt directory (../output/)
OUTPUT_PARENT=$(dirname "$PDBQT_DIR")

# Define intermediate and final output directories
INTERMEDIATE_DIR="$OUTPUT_PARENT/sdf_intermediate"
FINAL_DIR="$OUTPUT_PARENT/sdf_final"

# Run first script silently
python ./scripts/pdbqt2sdf_1.py "$PDBQT_DIR" >/dev/null 2>&1

# Ensure intermediate directory exists
if [ ! -d "$INTERMEDIATE_DIR" ]; then
    echo "Error: Intermediate directory not found at $INTERMEDIATE_DIR"
    exit 1
fi

# Run second script silently
python ./scripts/pdbqt2sdf_2.py "$INTERMEDIATE_DIR" >/dev/null 2>&1

echo ">>> Done! Final SDF files saved in: $FINAL_DIR"
