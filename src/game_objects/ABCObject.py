from abc import ABC, abstractmethod
from .coords2D import Coords2d

class ABCObject(ABC):

    @property
    @abstractmethod
    def coords(self) -> list[Coords2d]:
        pass

    @property
    @abstractmethod
    def is_closed(self) -> bool:
        pass
