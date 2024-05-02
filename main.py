import shutil
from updateablezipfile import UpdateableZipFile
from ModelParser import *
import os

done = False

# Open 3mf file and copy to zip
while not done:
    modelFileName = input("Name of 3mf file (without extension): ")

    try:
        shutil.copyfile(modelFileName + ".3mf", modelFileName + ".zip")
        done = True
    except:
        print("3mf file doesn't exist")

# Extract .model file from zip
with UpdateableZipFile(modelFileName + ".zip", "r") as f:
    with open('object_1.model', "wb") as file:
        file.write(f.read("3D/Objects/object_1.model"))

# Parse model file
modelParser = ModelParser()
modelParser.parse_from_file("object_1.model")

for face in modelParser.faces:
    f.filament = "8"

# Write model back to file
modelParser.object_to_model()

# Overwrite model file
shutil.copyfile("object_1_new.model", "object_1.model")

# Replace model file in zip
with UpdateableZipFile(modelFileName + ".zip", "a") as f:
    f.write("object_1.model", "3D/Objects/object_1.model")

# Rename back to 3MF and remove redundant files
shutil.copyfile(modelFileName + ".zip", modelFileName + ".3mf")
os.remove(modelFileName + ".zip")
os.remove("object_1.model")
os.remove("object_1_new.model")


