from game_objects.ABCObject import ABCObject
from game_objects.coords2D import Coords2d
import math

from const_wireframes import basic_square, basic_line
class Window:
    def __init__(self, max_x:float, max_y:float) -> None:
        self.__display_file = [basic_square, basic_line]
        self.__max_x = max_x
        self.__max_y = max_y
        self.__min_x = 0
        self.__min_y = 0
        self.__crt_center = Coords2d(max_x//2, max_y//2)

        self.__initial_x = self.__max_x
        self.__initial_y= self.__max_y

    @property
    def display_file(self) -> list[ABCObject]:
        return self.__display_file

    @property
    def max_x(self) -> float:
        return self.__max_x

    @property
    def max_y(self) -> float:
        return self.__max_y

    @property
    def min_x(self) -> float:
        return self.__min_x

    @property
    def min_y(self) -> float:
        return self.__min_y

    def move_x(self, delta:float) -> None:
        self.__max_x += delta 
        self.__min_x += delta

    def move_y(self, delta:float) -> None:
        self.__max_y += delta 
        self.__min_y += delta

    def zoom(self, delta:float) -> None:
        ratio = self.__initial_x/self.__initial_y
        dx = delta * ratio
        dy = delta * (1/ratio)
        self.__max_x += dx 
        self.__min_x -= dx 

        self.__max_y += dy
        self.__min_y -= dy