from .ABCObject import ABCObject
from .coords2D import Coords2d


class Point(ABCObject):
    def __init__(self, name : str, a:tuple[float], color=(0, 0, 0)) -> None:
        coords = [Coords2d(a[0], a[1])]
        super().__init__(name, color, coords)

    @property
    def is_closed(self) -> bool:
        return False