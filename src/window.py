from .game_objects.ABCObject import ABCObject
from .game_objects.coords2D import Coords2d
from .game_objects.cg_math import CgMath
from .const_wireframes import to_load


import math


class Window:
    def __init__(self, x_size : float, y_size : float) -> None:
        self.__display_file = to_load

        self.__size = Coords2d(x_size, y_size)
        self.__center = self.__scale / 2
        self.__up_vector = Coords2d(0, 1)

        self.__min_x = 0
        self.__min_y = 0

        self.__ratio = self.__size.x/self.__size.y

        # For checking names in constant time
        self.__names_map = {}
        for obj in self.__display_file:
            self.__names_map[obj.name] = obj

        
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

    def add_to_display_file(self, obj : ABCObject):
        self.__display_file.append(obj)
        self.__names_map[obj.name] = obj

    def get_obj(self, name : str):
        if name in self.__names_map:
            return self.__names_map[name]
        return False

    def update_normalized(self):
        abs_up = Coords2d(1, 0)

        # Rotating
        angle = math.acos(abs_up.x * self.__up_vector.x + abs_up.y * self.__up_vector.y)
        print(angle)
        degrees = (angle/math.pi) * 180
        translate_center_m = CgMath.get_translation_matrix(self.__center.x, self.__center.y)
        rotation_m = CgMath.get_rotation_matrix(degrees)
        center_rotation_m = CgMath.matrix_multiply(translate_center_m, rotation_m)

        # Normalizing -1, 1
        scale_x = 1/self.__size.x
        scale_y = 1/self.__size.y
        scale_m = CgMath.get_scale_matrix(scale_x, scale_y)
        translate_m = CgMath.get_translation_matrix(-1, -1)
        normalization_m = CgMath.matrix_multiply(scale_m, translate_m)

        full_normalize_transform = CgMath.matrix_multiply(center_rotation_m, normalization_m)

        for obj in self.__display_file:
            obj.update_normalized(full_normalize_transform)

