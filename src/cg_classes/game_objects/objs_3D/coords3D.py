from __future__ import annotations
import math

class Coords3d():
    def __init__(self, x:float, y:float, z:float) -> None:
        self.__x = x
        self.__y = y 
        self.__z = z

    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y

    @property
    def z(self) -> float:
        return self.__z

    @x.setter
    def x(self, new:float) -> None:
        self.__x = new

    @y.setter
    def y(self, new:float) -> None:
        self.__y = new

    @z.setter
    def z(self, new:float) -> None:
        self.__z = new
    
    def __add__(self, point:Coords3d) -> Coords3d:
        x = self.x + point.x
        y = self.y + point.y
        z = self.z + point.z
        return(Coords3d(x, y, z)) 

    def __itruediv__(self, point:Coords3d) -> Coords3d:
        x = self.x / point.x
        y = self.y / point.y
        z = self.y / point.y
        return(Coords3d(x, y, z)) 

    def __mul__(self, point:Coords3d) -> Coords3d:
        x = self.x * point.x
        y = self.y * point.y
        z = self.y * point.y
        return(Coords3d(x, y, z)) 

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
