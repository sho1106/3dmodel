from stl import mesh
import sys
import numpy as np
import model_manager


class STLModel:
    def __init__(self, filename):
        model = mesh.Mesh.from_file(filename)

        self.triangles = []
        self.points = []
        #self.points = np.concatenate([model.v0, model.v1, model.v2])
        #self.points = np.unique(self.points, axis=0)
        #self.points = [p for p in self.points]

        for tri in model.vectors:
            self.points.append(tri[0])
            self.points.append(tri[1])
            self.points.append(tri[2])
            v0 = len(self.points)-3
            v1 = len(self.points)-2
            v2 = len(self.points)-1
            self.triangles.append([v0, v1, v2])
        

def main():
    
    model = STLModel("egg.stl")
    print(len(model.points))
    print(len(model.triangles))

    maker = model_manager.VRMLModelMaker()
    vrml_model = model_manager.TriangleMesh(model.points, model.triangles, [1, 1, 1], 0.9)
    strs = vrml_model.to_str(maker)
    maker.dump("egg", strs)


    return True

if __name__ == "__main__":
    sys.exit(int(main() or 0))