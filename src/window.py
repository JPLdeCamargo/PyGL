from .game_objects.ABCObject import ABCObject
from .game_objects.coords2D import Coords2d
from .game_objects.cg_math import CgMath
from .const_wireframes import to_load


import math


class Window:
    def __init__(self, x_size : float, y_size : float) -> None:
        self.__display_file = to_load

        self.__size = Coords2d(x_size, y_size)
        self.__center = Coords2d(x_size/2, y_size/2)
        self.__up_vector = Coords2d(0, 1)
        self.__right_vector = Coords2d(1, 0)

        self.__ratio = self.__size.x/self.__size.y

        # For checking names in constant time
        self.__names_map = {}
        for obj in self.__display_file:
            self.__names_map[obj.name] = obj

        # Filling normalized coords of all objects
        self.update_normalized()
        
    @property
    def display_file(self) -> list[ABCObject]:
        return self.__display_file

    def move_x(self, delta:float) -> None:
        scale = self.__size.x
        delta = (delta * scale)/1000
        delta_vector = Coords2d(self.__right_vector.x * delta,
                                self.__right_vector.y * delta)
        self.__center += delta_vector

        self.update_normalized()

    def move_y(self, delta:float) -> None:
        scale = self.__size.y
        delta = (delta * scale)/1000
        delta_vector = Coords2d(self.__up_vector.x * delta,
                                self.__up_vector.y * delta)
        self.__center += delta_vector

        self.update_normalized()

    def zoom(self, delta:float) -> None:
        scale = self.__size.x
        delta = (delta * scale)/1000

        dx = delta * self.__ratio
        dy = delta

        self.__size.x += dx 
        self.__size.y += dy

        self.update_normalized()

    def rotate(self, angle:float):
        rotation_m = CgMath.get_rotation_matrix(angle)
        homogenous_up = [[self.__up_vector.x, self.__up_vector.y, 1]]
        homogenous_right = [[self.__right_vector.x, self.__right_vector.y, 1]]

        new_up_m = CgMath.matrix_multiply(homogenous_up, rotation_m)
        new_right_m = CgMath.matrix_multiply(homogenous_right, rotation_m)

        self.__up_vector.x = new_up_m[0][0]
        self.__up_vector.y = new_up_m[0][1]

        self.__right_vector.x = new_right_m[0][0]
        self.__right_vector.y = new_right_m[0][1]

        self.update_normalized()

    def add_to_display_file(self, obj : ABCObject):
        self.__display_file.append(obj)
        self.__names_map[obj.name] = obj

    def get_obj(self, name : str):
        if name in self.__names_map:
            return self.__names_map[name]
        return False

    def update_normalized(self):
        abs_up = Coords2d(0, 1)

        # Rotating
        angle = math.acos(abs_up.x * self.__up_vector.x + abs_up.y * self.__up_vector.y)
        degrees = (angle/math.pi) * 180
        if self.__up_vector.x < 0:
            degrees = 360 - degrees

        translate_center_m = CgMath.get_translation_matrix(-self.__center.x, -self.__center.y)
        rotation_m = CgMath.get_rotation_matrix(-degrees)
        center_rotation_m = CgMath.matrix_multiply(translate_center_m, rotation_m)

        # Normalizing -1, 1
        scale_x = 2/self.__size.x
        scale_y = 2/self.__size.y
        scale_m = CgMath.get_scale_matrix(scale_x, scale_y)
        # translate_m = CgMath.get_translation_matrix(-1, -1)
        # normalization_m = CgMath.matrix_multiply(scale_m, translate_m)

        full_normalize_transform = CgMath.matrix_multiply(center_rotation_m, scale_m)

        for obj in self.__display_file:
            obj.update_normalized(full_normalize_transform)

