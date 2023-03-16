from __future__ import annotations
import math

class Coords2d():
    def __init__(self, x:int, y:int) -> None:
        self.__x = x
        self.__y = y 

    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, new:int) -> None:
        self.__x = new

    @y.setter
    def y(self, new:int) -> None:
        self.__y = new
    
    def __add__(self, point:Coords2d) -> Coords2d:
        x = self.x + point.x
        y = self.y + point.y
        return(Coords2d(x, y)) 

    def __itruediv__(self, point:Coords2d) -> Coords2d:
        x = self.x // point.x
        y = self.y // point.y
        return(Coords2d(x, y)) 

    def __mul__(self, point:Coords2d) -> Coords2d:
        x = math.floor(self.x * point.x)
        y = math.floor(self.y * point.y)
        return(Coords2d(x, y)) 

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
