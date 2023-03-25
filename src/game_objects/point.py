from .ABCObject import ABCObject
from .coords2D import Coords2d


class Point(ABCObject):
    def __init__(self, name : str, a:tuple[float]) -> None:
        super().__init__(name)
        self.__coords = [Coords2d(a[0], a[1])]

    @property
    def coords(self) -> list[Coords2d]:
        return self.__coords

    @property
    def is_closed(self) -> bool:
        return False