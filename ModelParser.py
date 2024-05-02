class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Face:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.filament = None


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
            if line.__contains__('vertex'):
                xInd = line.index('x=') + 3
                yInd = line.index('y=') + 3
                zInd = line.index('z=') + 3
                x = float(self.getValue(line, xInd))
                y = float(self.getValue(line, yInd))
                z = float(self.getValue(line, zInd))
                self.vertices.append(Vertex(x, y, z))
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
