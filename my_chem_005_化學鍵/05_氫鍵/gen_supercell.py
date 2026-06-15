from pymatgen.core import Structure
from pymatgen.io.xyz import XYZ

s = Structure.from_file("NaHCO3.cif")
s.make_supercell([2, 2, 2])

# Write to PDB
s.to(fmt="pdb", filename="NaHCO3_supercell.pdb")
print("Supercell generated with", len(s), "atoms.")
