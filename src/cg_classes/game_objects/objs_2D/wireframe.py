from .coords2D import Coords2d
from .ABCObject import ABCObject
from .cg_math_2D import CgMath2D

class WireFrame(ABCObject):
    def __init__(self, name : str, is_closed:bool, raw_coords: list[tuple[float]], color=(0, 0, 0)) -> None:
        # List with every point of the polygon
        # order matters, first point connect to the second one
        # last point connected to the first one
        coords = []
        for point in raw_coords:
            coords.append(Coords2d(point[0], point[1]))
        
        super().__init__(name, color, coords)

        self.__is_closed = is_closed

    @property
    def is_closed(self) -> bool:
        return self.__is_closed

    def to_wavefront(self) -> str:
        wavefront_str = (f"{self.name}\n"
                         f"c {self.color[0]} {self.color[1]} {self.color[2]}\n")
        for point in self.coords:
            wavefront_str += f"f {point.x} {point.y}\n"

        val = 1 if self.__is_closed else 0 
        wavefront_str += f"IsClosed {val}\n"

        return wavefront_str

    def update_clipping(self):
        self._clipped_coords = CgMath.shuterland_hodgeman_polygon_clipping(self.normalized_coords, self.__is_closed)