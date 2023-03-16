from .coords2D import Coords2d
from .ABCObject import ABCObject

class Line(ABCObject):
    def __init__(self, a:tuple[float], b:tuple[float]) -> None:
        self.__coords = [Coords2d(a[0], a[1]), Coords2d(b[0], b[1])]

    @property
    def coords(self) -> list[Coords2d]:
        return self.__coords

    @property
    def is_closed(self) -> bool:
        return False

        