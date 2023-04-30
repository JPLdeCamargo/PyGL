from .coords2D import Coords2d
from .ABCObject import ABCObject
from .cg_math_2D import CgMath2D

class Line(ABCObject):
    def __init__(self, name : str, a:tuple[float], b:tuple[float], color=(0,0,0)) -> None:
        coords = [Coords2d(a[0], a[1]), Coords2d(b[0], b[1])]
        super().__init__(name, color, coords)

    @property
    def is_closed(self) -> bool:
        return False

    def to_wavefront(self) -> str:
        return (f"{self.name}\n"
                f"c {self.color[0]} {self.color[1]} {self.color[2]}\n" 
                f"l {self.coords[0].x} {self.coords[0].y}\n"
                f"l {self.coords[1].x} {self.coords[1].y}\n")

    def update_clipping(self):
        a = self.normalized_coords[0]
        b = self.normalized_coords[1]
        self._clipped_coords = CgMath.cohen_shuterland_line_clipping(a, b)