from .coords2D import Coords2d
from .ABCObject import ABCObject

class WireFrame(ABCObject):
    def __init__(self, coords: list[Coords2d]) -> None:
        # List with every point of the polygon
        # order matters, first point connect to the second one
        # last point connected to the first one
        self.__coords = coords

    @property
    def coords(self) -> list[Coords2d]:
        return self.__coords