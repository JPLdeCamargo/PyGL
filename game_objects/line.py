from .coords2D import Coords2d
from .ABCObject import ABCObject

class Line(ABCObject):
    def __init__(self, a:Coords2d, b:Coords2d) -> None:
        self.__coords = [a, b]

    @property
    def coords(self) -> list[Coords2d]:
        return self.__coords

        