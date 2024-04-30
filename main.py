import shutil
from updateablezipfile import UpdateableZipFile
from Bio.PDB import *
from ModelParser import *
import os

done = False

while not done:
    modelFileName = input("Name of 3mf file (without extension): ")

    try:
        shutil.copyfile(modelFileName + ".3mf", modelFileName + ".zip")
        done = True
    except:
        print("3mf file doesn't exist")

with UpdateableZipFile(modelFileName + ".zip", "r") as f:
    with open('object_1.model', "wb") as file:
        file.write(f.read("3D/Objects/object_1.model"))

modelParser = ModelParser()
modelParser.parse_from_file("object_1.model")

for face in modelParser.faces:
    face.filament = "8"

modelParser.object_to_model()

shutil.copyfile("object_1_new.model", "object_1.model")
os.remove("object_1_new.model")

with UpdateableZipFile(modelFileName + ".zip", "a") as f:
    f.write("object_1.model", "3D/Objects/object_1.model")

shutil.copyfile(modelFileName + ".zip", modelFileName + ".3mf")
os.remove("test.zip")
os.remove("object_1.model")


