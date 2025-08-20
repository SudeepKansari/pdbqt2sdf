# pdbqt2sdf  

A Repository to convert ligands in pdbqt to sdf format.

Steps for conversion:

1. Install the environment

```bash
$ conda env create -f pdbqt2sdf.yml
```

2. Make the shell script executable

```bash
$ chmod +x pdbqt2sdf_conversion.sh
```

3. Run the conversion

```bash
$ bash pdbqt2sdf_conversion.sh <path_to_pdbqt_directory>
```

The script will convert all pdbqt ligands found in the specified directory into sdf format.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
