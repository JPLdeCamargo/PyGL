from __future__ import annotations
import math

class Coords2d():
    def __init__(self, x:float, y:float) -> None:
        self.__x = x
        self.__y = y 

    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y

    @x.setter
    def x(self, new:float) -> None:
        self.__x = new

    @y.setter
    def y(self, new:float) -> None:
        self.__y = new
    
    def __add__(self, point:Coords2d) -> Coords2d:
        x = self.x + point.x
        y = self.y + point.y
        return(Coords2d(x, y)) 

    def __itruediv__(self, point:Coords2d) -> Coords2d:
        x = self.x / point.x
        y = self.y / point.y
        return(Coords2d(x, y)) 

    def __mul__(self, point:Coords2d) -> Coords2d:
        x = self.x * point.x
        y = self.y * point.y
        return(Coords2d(x, y)) 

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
