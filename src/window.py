from game_objects.ABCObject import ABCObject

from const_wireframes import to_load
class Window:
    def __init__(self, max_x:float, max_y:float) -> None:
        self.__display_file = to_load
        self.__max_x = max_x
        self.__max_y = max_y
        self.__min_x = 0
        self.__min_y = 0

        self.__ratio = max_x/max_y


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
        scale = self.__max_x - self.__min_x
        delta = (delta * scale)/1000
        self.__max_x += delta 
        self.__min_x += delta

    def move_y(self, delta:float) -> None:
        scale = self.__max_x - self.__min_x
        delta = (delta * scale)/1000
        self.__max_y += delta 
        self.__min_y += delta

    def zoom(self, delta:float) -> None:
        scale = self.__max_x - self.__min_x
        delta = (delta * scale)/1000
        dx = delta * self.__ratio
        dy = delta
        self.__max_x += dx 
        self.__min_x -= dx 

        self.__max_y += dy
        self.__min_y -= dy