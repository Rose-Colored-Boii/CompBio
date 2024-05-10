import numpy as np
import pymeshlab
import math
from scipy.spatial import KDTree

class Vertex:
    def __init__(self, x, y, z, index):
        self.x = x
        self.y = y
        self.z = z
        self.color = None
        self.index = index

class Face:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.filament = None
        self.color = None


# Class to parse .model files
class ModelParser:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.fileName = ""

    # Helper function to extract value from specific field
    def getValue(self, string, index):
        value = ""
        while string[index] != "\"":
            value += string[index]
            index += 1
        return value

    def parse_from_file(self, fileName):
        file = open(fileName)
        for line in file:
            # Extract vertices of model
            indexCount = 0
            if line.__contains__('vertex'):
                xInd = line.index('x=') + 3
                yInd = line.index('y=') + 3
                zInd = line.index('z=') + 3
                x = float(self.getValue(line, xInd))
                y = float(self.getValue(line, yInd))
                z = float(self.getValue(line, zInd))
                self.vertices.append(Vertex(x, y, z, indexCount))
                indexCount += 1
            # Extract faces of model
            elif line.__contains__('triangle '):
                v1Ind = line.index('v1') + 4
                v2Ind = line.index('v2') + 4
                v3Ind = line.index('v3') + 4
                v1 = self.vertices[int(self.getValue(line, v1Ind))]
                v2 = self.vertices[int(self.getValue(line, v2Ind))]
                v3 = self.vertices[int(self.getValue(line, v3Ind))]
                self.faces.append(Face(v1, v2, v3))
        self.fileName = fileName

    def load_color_data(self, GLTF):
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh("1ce6.pdb")
        mesh = ms.current_mesh()
        vertices = mesh.vertex_matrix()
        ms.load_new_mesh(GLTF)
        for i in range(len(ms)):
            ms.set_current_mesh(i)
            mesh = ms.current_mesh()
            vertices = mesh.vertex_matrix()
            colors = mesh.vertex_color_array()
            tree = KDTree(vertices)
            for vertex in np.array(self.vertices):
                closest_index = tree.query([vertex.x, vertex.y, vertex.z])[1]
                vertex.color = colors[closest_index]
        for face in self.faces:
            colors = [face.v1.color, face.v2.color, face.v3.color]
            color_counts = {}
            for color in colors:
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1
            maxCount = -1
            faceColor = None
            for color, count in color_counts.items():
                if count > maxCount:
                    maxCount = count
                    faceColor = color
            face.color = faceColor
        colors = []
        for face in self.faces:
            if face.color not in colors:
                colors.append(face.color)
        print(colors)

    def object_to_model(self):
        # Write changes back to file
        file = open(self.fileName)
        newFile = open(self.fileName[:-6] + "_new.model", "w+")
        faceNum = 0
        for line in file:
            if not line.__contains__('triangle '):
                newFile.write(line)
            else:
                if line.__contains__("paint_color"):
                    newFile.write(line)
                    faceNum += 1
                else:
                    # If filament field changed, write new paint color out to model
                    filament = self.faces[faceNum].filament
                    if filament is not None:
                        newLine = line[:-3] + " paint_color=\"" + filament + "\"" + line[-3:]
                        newFile.write(newLine)
                    else:
                        newFile.write(line)
                    faceNum += 1
