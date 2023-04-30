from .ABCObject3D import ABCObject3D
from .coords3D import Coords3d


class Point3D(ABCObject3D):
    def __init__(self, name : str, a:tuple[float], color=(0, 0, 0)) -> None:
        coords = [Coords3d(a[0], a[1], a[3])]
        super().__init__(name, color, coords)

    @property
    def is_closed(self) -> bool:
        return False

    def to_wavefront(self) -> str:
        return(f"{self.name}\n"
               f"c {self.color[0]} {self.color[1]} {self.color[2]}\n" 
               f"p {self.coords[0].x} {self.coords[0].y} {self.coords[0].z}\n")

    def update_clipping(self):
        self._clipped_coords = self.normalized_coords
