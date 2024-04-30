import shutil
from Bio.PDB import *
from zipfile import ZipFile
from ModelParser import *

done = False

while not done:
    modelFileName = input("Name of 3mf file (without extension): ")

    try:
        shutil.copyfile(modelFileName + ".3mf", modelFileName + ".zip")
        done = True
    except:
        print("3mf file doesn't exist")

with ZipFile(modelFileName + ".zip", "r") as f:
    with open('object_1.model', "wb") as file:
        file.write(f.read("3D/Objects/object_1.model"))

modelParser = ModelParser()
modelParser.parse_from_file("object_1.model")

parser = PDBParser()
structure = parser.get_structure("test", "test.pdb").get_atoms()
pass
