from game_objects.ABCObject import ABCObject
from game_objects.coords2D import Coords2d
import math

from const_wireframes import basic_square
class Window:
    def __init__(self, max_x:int, max_y:int) -> None:
        self.__display_file = [basic_square]
        self.__max_x = max_x
        self.__max_y = max_y
        self.__min_x = 0
        self.__min_y = 0
        self.__crt_center = Coords2d(max_x//2, max_y//2)

    @property
    def display_file(self) -> list[ABCObject]:
        return self.__display_file

    @property
    def max_x(self) -> int:
        return self.__max_x

    @property
    def max_y(self) -> int:
        return self.__max_y

    @property
    def min_x(self) -> int:
        return self.__min_x

    @property
    def min_y(self) -> int:
        return self.__min_y

    def move_x(self, delta:int) -> None:
        self.__max_x += delta 
        self.__min_x += delta

    def move_y(self, delta:int) -> None:
        self.__max_y += delta 
        self.__min_y += delta

    def zoom(self, delta:int) -> None:
        x = self.__max_x - self.__min_x
        y = self.__max_y - self.__min_y
        ratio = x/y
        dx = math.floor(delta * ratio)
        dy = math.floor(delta * (1/ratio))
        self.__max_x += dx 
        self.__min_x -= dx 

        self.__max_y += dy
        self.__min_y -= dy