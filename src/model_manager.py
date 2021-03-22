# -*- coding: shift_jis -*-
import os

class Model:
    def __init__(self, color, transparency=None):
        if color is None:
            self._color = None
        else:
            assert(isinstance(color, list))
            assert(len(color)==3)
            self._color = color
        self._trans = transparency

    def to_str(self, maker):
        assert(isinstance(maker, VRMLModelMaker))
        if self._color is not None:
            return maker._color(self._color, self._trans)

        return ""

class Sphere:
    def __init__(self, center, radius, color):
        assert(isinstance(radius, float))
        assert(isinstance(center, list))
        assert(len(center)==3)
        assert(radius>0)

        self._center = center
        self._radius = radius

        self._color = Model(color)

    def to_str(self, maker):
        assert(isinstance(maker, VRMLModelMaker))
        return maker.to_str_sphere(self._center, self._radius, self._color)

class Lines:
    def __init__(self, points, pairs, color):
        assert(isinstance(points, list))
        assert(isinstance(pairs, list))

        self._color = Model(color)

        for pair in pairs:
            assert(len(pair)==2)
            pre = pair[0]
            nxt = pair[1]

            assert(len(points)>pre)
            assert(len(points)>nxt)
        self._points = points
        self._pairs = pairs
    
    def to_str(self, maker):
        assert(isinstance(maker, VRMLModelMaker))
        return maker.to_str_lines(self._points, self._pairs, self._color)

class TriangleMesh:
    def __init__(self, points, triangles, color, transparency=None):

        self._color = Model(color, transparency)
        
        self._points = points
        self._tri = triangles

    def to_str(self, maker):
        assert(isinstance(maker, VRMLModelMaker))
        return maker.to_str_poly(self._points, self._tri, self._color)


class VRMLModelMaker:
    def __init__(self):
        pass

    def _tab_str(self, num):
        return " "*num

    def _transform(self, translation, format):
        assert(isinstance(translation, list))
        assert(len(translation)==3)
        out = "Transform {\ntranslation "
        out += "{} {} {}\n".format(*translation)
        return out + "{}".format(format) + "}\n"

    def _children(self, format):
        return "children [\n{}]\n".format(format)

    def _color(self, color, transparency=None):
        out = "appearance Appearance {\nmaterial Material {\ndiffuseColor "
        out += "{} {} {}".format(*color) + "\n"
        if transparency is not None:
            out += "transparency {}\n".format(transparency)
        out += "}\n}\n"
        return out

    def _shape(self, geometry_type, format, color):
        out = "Shape {\ngeometry " + geometry_type + " {\n"
        out += format + "}\n"
        out += color.to_str(self) + "}\n"
        return out

    def _sphere(self, radius, color):
        return self._shape("Sphere", "radius {}\n".format(radius), color)

    def _lines(self, points, pairs, color):
        assert(len(points)>1)
        assert(len(pairs)>0)

        format = "coord Coordinate {\npoint ["
        format += "{} {} {}".format(*points[0])
        for point in points[1:]:
            format += ",\n{} {} {}".format(*point)
        format += "\n]\n}"
        format += "coordIndex [\n"
        format += "{}, {}, -1".format(*pairs[0])
        if len(pairs)>1:
            for pair in pairs[1:]:
                format += "\n,{}, {}, -1".format(*pair)
        format += "\n]\n"

        return self._shape("IndexedLineSet", format, color)
        

    def _list(self, strlist):
        out = "";
        for str in strlist:
            out += str + "\n";
        return out

    def to_str_sphere(self, center, radius, color):
        assert(isinstance(radius, float))
        assert(isinstance(center, list))
        assert(len(center)==3)
        assert(radius>0)

        strs = self._sphere(radius, color)
        strs = self._transform(center, self._children(strs))

        return strs
    
    def dump(self, filename, strs):

        if len(filename) < 4 or ".wrl" not in filename[-4]:
            filename += ".wrl"

        with open(filename, "w") as f:
            f.write("#VRML V2.0 utf8\n")
            f.write(strs)

    def to_str_lines(self, points, pairs, color):
        strs = self._lines(points, pairs, color)
        return strs

    def to_str_poly(self, points, polygon, color):
        assert(len(points)>1)
        assert(len(polygon)>0)

        format = "coord Coordinate {\npoint ["
        format += "{} {} {}".format(*points[0])
        for point in points[1:]:
            format += ",\n{} {} {}".format(*point)
        format += "\n]\n}"
        format += "coordIndex [\n"
        format += ",".join(map(lambda x: str(x), polygon[0])) + ", -1"
        if len(polygon)>1:
            for poly in polygon[1:]:
                format += "\n," + ",".join(map(lambda x:str(x), poly)) + ", -1"
        format += "\n]\n"

        return self._shape("IndexedFaceSet", format, color)



    def to_str_models(self, models):
        out = ""
        for model in models:
            out += model.to_str(self)
        return out

if __name__=="__main__":

    sphere = Sphere([1, 2, 3], 0.5, [1, 0, 0])
    lines = Lines(
        [[0, 0, 0],[1, 0, 0]],
        [[0, 1]],
        [0, 1, 0]
        )
    maker = VRMLModelMaker()
    
    strs = sphere.to_str(maker)
    maker.dump("sphere", strs)
    strs = lines.to_str(maker)
    maker.dump("lines", strs)
    strs = maker.to_str_models([sphere, lines])
    maker.dump("sphere_lines", strs)