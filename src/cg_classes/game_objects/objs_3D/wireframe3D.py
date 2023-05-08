from .coords3D import Coords3d
from .ABCObject3D import ABCObject3D
from .cg_math_3D import CgMath3D

class WireFrame3D(ABCObject3D):
    def __init__(self, name:str, faces:list[tuple[int]], raw_vertices: list[tuple[float]], color=(0, 0, 0)) -> None:
        # List with every point of the polygon
        # order matters, first point connect to the second one
        # last point connected to the first one
        coords = []
        for point in raw_vertices:
            coords.append(Coords3d(point[0], point[1], point[2]))
        
        super().__init__(name, color, coords)

        self.__faces = faces

    @property
    def faces(self) -> list[tuple[int]]:
        return self.__faces

    def to_wavefront(self) -> str:
        wavefront_str = (f"{self.name}\n"
                         f"c {self.color[0]} {self.color[1]} {self.color[2]}\n")
        for point in self.coords:
            wavefront_str += f"v {point.x} {point.y} {point.z}\n"

        for edge in self.__edges:
            wavefront_str += f"e {edge[0]+1} {edge[1]+1}\n"

        return wavefront_str

    def update_clipping(self):
        self._clipped_coords = []
        for face in self.__faces:
            face_coords = []
            for i in range(len(face)):
                face_coords.append(self.normalized_coords[face[i]])
            clipped = CgMath3D.shuterland_hodgeman_polygon_clipping(face_coords)
            if len(clipped) != 0:
                self._clipped_coords.append(clipped)


