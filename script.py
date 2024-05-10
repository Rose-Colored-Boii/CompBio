import pymeshlab

ms = pymeshlab.MeshSet()

done = False

modelFileName = ""

# Open glb file
while not done:
    modelFileName = input("Name of glb file (without extension): ")

    try:
        ms.load_new_mesh(modelFileName + ".glb", load_in_a_single_layer=True)
        done = True
    except:
        print("glb file doesn't exist")

# Saves mesh as obj file with vertex color data
ms.save_current_mesh(modelFileName + ".obj")
