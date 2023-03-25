from .coords2D import Coords2d
from .ABCObject import ABCObject

class WireFrame(ABCObject):
    def __init__(self, name : str, is_closed:bool, raw_coords: list[tuple[float]]) -> None:
        super().__init__(name)
        # List with every point of the polygon
        # order matters, first point connect to the second one
        # last point connected to the first one
        self.__coords = []
        for point in raw_coords:
            self.__coords.append(Coords2d(point[0], point[1]))
        
        self.__is_closed = is_closed

    @property
    def coords(self) -> list[Coords2d]:
        return self.__coords

    @property
    def is_closed(self) -> bool:
        return self.__is_closed