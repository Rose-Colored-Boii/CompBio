from Bio.PDB import *
parser = PDBParser()
structure = parser.get_structure("1ce6", "1ce6.pdb")

for model in structure:
    chain = model["B"]
    for residue in chain:
        for atom in residue:
            print(atom.id, atom.get_coord())
