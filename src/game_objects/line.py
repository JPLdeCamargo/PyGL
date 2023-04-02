from .coords2D import Coords2d
from .ABCObject import ABCObject

class Line(ABCObject):
    def __init__(self, name : str, a:tuple[float], b:tuple[float], color=(0,0,0)) -> None:
        coords = [Coords2d(a[0], a[1]), Coords2d(b[0], b[1])]
        super().__init__(name, color, coords)

    @property
    def is_closed(self) -> bool:
        return False

        