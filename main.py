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

modelName = ""

# Extract .model file from zip
with UpdateableZipFile(modelFileName + ".zip", "r") as f:
    fileNames = f.namelist()
    for name in fileNames:
        if name.endswith(".model") and name.startswith("3D/Objects"):
            file = open("temp.model", "wb")
            file.write(f.read(name))
            modelName = name
            break

# Parse model file
modelParser = ModelParser()
modelParser.parse_from_file("temp.model")

modelParser.load_color_data("1ce6.glb")

# Write model back to file
modelParser.object_to_model()

# Overwrite model file
shutil.copyfile("temp_new.model", "temp.model")

# Replace model file in zip
with UpdateableZipFile(modelFileName + ".zip", "a") as f:
    f.write("temp.model", name)

# Rename back to 3MF and remove redundant files
shutil.copyfile(modelFileName + ".zip", modelFileName + ".3mf")
os.remove(modelFileName + ".zip")
os.remove("temp.model")
os.remove("temp_new.model")


