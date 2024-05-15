import pymeshlab
import os

done = False
name = input("Enter UniProt name / ID: ")

os.system("chimerax --nogui --exit --nostatus --script \"SubChains.py " + name + "\"")

# Load mesh
ms = pymeshlab.MeshSet()
ms.load_new_mesh(name + ".glb", load_in_a_single_layer=True)

# Saves mesh as obj file with vertex color data
ms.save_current_mesh(name + ".obj")
