from .game_objects.objs_3D.ABCObject3D import ABCObject3D
from .game_objects.objs_3D.coords3D import Coords3d
from .game_objects.objs_3D.cg_math_3D import CgMath3D

from .game_objects.objs_2D.coords2D import Coords2d
from .game_objects.objs_2D.cg_math_2D import CgMath2D

from .game_objects.objs_3D.wireframe3D import WireFrame3D

import math


class Window:
    def __init__(self, x_size : float, y_size : float, to_load:list[ABCObject3D]) -> None:
        self.__display_file = [WireFrame3D("Lindo", True,
                                           [(0,1),(1,2),(2,3),(3,0),
                                            (0,4),(1,5),(2,6),(3,7),
                                            (4,5),(5,6),(6,7),(7,4)], 
                                           [(0,0,0),(3500,0,0),(3500,0,3500),(0,0,3500),
                                            (0,3500,0),(3500,3500,0),(3500,3500,3500),(0,3500,3500)])]
        self.__display_file[0].rotate(30,Coords3d(1750,1750,1750),Coords3d(1,1,1))

        self.__size = Coords2d(x_size, y_size)
        self.__center = Coords3d(x_size/2, y_size/2, 0)
        self.__up_vector = Coords3d(0, 1, 0)
        self.__right_vector = Coords3d(1, 0, 0)
        self.__front_vector = Coords3d(0, 0, 1)

        self.__ratio = self.__size.x/self.__size.y

        # For checking names in constant time
        self.__names_map = {}
        for obj in self.__display_file:
            self.__names_map[obj.name] = obj

        # Filling normalized coords of all objects
        self.update_world()
        self.update_normalized()
        
    @property
    def display_file(self) -> list[ABCObject3D]:
        return self.__display_file

    def move_x(self, delta:float) -> None:
        scale = self.__size.x
        delta = (delta * scale)/1000
        delta_vector = Coords3d(self.__right_vector.x * delta,
                                self.__right_vector.y * delta,
                                self.__right_vector.z * delta)
        self.__center += delta_vector

        self.update_world()
        self.update_normalized()

    def move_y(self, delta:float) -> None:
        scale = self.__size.y
        delta = (delta * scale)/1000
        delta_vector = Coords3d(self.__up_vector.x * delta,
                                self.__up_vector.y * delta,
                                self.__up_vector.z * delta)
        self.__center += delta_vector

        self.update_world()
        self.update_normalized()

    def zoom(self, delta:float) -> None:
        scale = self.__size.x
        delta = (delta * scale)/1000

        dx = delta * self.__ratio
        dy = delta

        self.__size.x += dx 
        self.__size.y += dy

        self.update_world()
        self.update_normalized()

    def rotate(self, angle:float, rotation_vector:tuple[float]):
        rotation_vector = Coords3d(rotation_vector[0], rotation_vector[1], rotation_vector[2])
        # Align rotation vector to xy plane
        angle_to_x_axis = math.asin(rotation_vector.z)
        angle_to_x_axis = (angle_to_x_axis/math.pi) * 180
        to_xy_plane =  CgMath3D.get_rotation_matrix_x(angle_to_x_axis)

        # Align rotation vector to y axis
        angle_to_y_axis = math.asin(rotation_vector.x)
        angle_to_y_axis = (angle_to_y_axis/math.pi) * 180
        to_y_axis =  CgMath3D.get_rotation_matrix_z(angle_to_y_axis)

        #Rotate the desired angle
        actual_rotation = CgMath3D.get_rotation_matrix_y(angle)

        # Redo previous transformations
        redo_y =  CgMath3D.get_rotation_matrix_z(-angle_to_y_axis)
        redo_xy =  CgMath3D.get_rotation_matrix_x(-angle_to_x_axis)

        rotation_m = CgMath3D.matrix_multiply(to_xy_plane, to_y_axis)
        rotation_m = CgMath3D.matrix_multiply(rotation_m, actual_rotation)
        rotation_m = CgMath3D.matrix_multiply(rotation_m, redo_y)
        rotation_m = CgMath3D.matrix_multiply(rotation_m, redo_xy)
        
        self.__up_vector = self.__transform_vector(self.__up_vector, rotation_m)
        self.__right_vector = self.__transform_vector(self.__right_vector, rotation_m)
        self.__front_vector = self.__transform_vector(self.__front_vector, rotation_m)

        # rotation_m = CgMath3D.matrix_multiply(rotation_m, CgMath3D.get_translation_matrix(-self.__center.x, -self.__center.y, -self.__center.z))
        # rotation_m = CgMath3D.matrix_multiply(CgMath3D.get_translation_matrix(self.__center.x, self.__center.y, self.__center.z), rotation_m)
        # self.__center = 

        self.update_world()
        self.update_normalized()

    def __transform_vector(self, v:Coords3d, matrix):
        homogenous_v = [[v.x, v.y, v.z, 1]]
        new_v_m = CgMath3D.matrix_multiply(homogenous_v, matrix)

        v.x = new_v_m[0][0]
        v.y = new_v_m[0][1]
        v.z = new_v_m[0][2]

        return v


    def add_to_display_file(self, obj : ABCObject3D):
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
        print(self.__up_vector, self.__right_vector, self.__front_vector)
        if self.__up_vector.x < 0 or self.__right_vector.x < 0 or self.__front_vector.x < 0:
            degrees = 360 - degrees

        translate_center_m = CgMath2D.get_translation_matrix(-self.__center.x, -self.__center.y)
        rotation_m = CgMath2D.get_rotation_matrix(-degrees)
        center_rotation_m = CgMath2D.matrix_multiply(translate_center_m, rotation_m)

        # Normalizing -1, 1
        scale_x = 2/self.__size.x
        scale_y = 2/self.__size.y
        scale_m = CgMath2D.get_scale_matrix(scale_x, scale_y)
        # translate_m = CgMath2D.get_translation_matrix(-1, -1)
        # normalization_m = CgMath2D.matrix_multiply(scale_m, translate_m)

        full_normalize_transform = CgMath2D.matrix_multiply(center_rotation_m, scale_m)

        for obj in self.__display_file:
            obj.update_normalized(full_normalize_transform)

    def update_world(self):
        n_normal = self.__front_vector
        d = math.sqrt(pow(n_normal.x, 2) + pow(n_normal.y, 2) + pow(n_normal.z, 2))
        n_normal.x /= d
        n_normal.y /= d
        n_normal.z /= d

        to_center = CgMath3D.get_translation_matrix(-self.__center.x, -self.__center.y, -self.__center.z)
        from_center = CgMath3D.get_translation_matrix(self.__center.x, self.__center.y, self.__center.z)

        # Align rotation vector to xy plane
        angle_to_zx_axis = math.asin(n_normal.y)
        angle_to_zx_axis = (angle_to_zx_axis/math.pi) * 180
        to_zx_plane =  CgMath3D.get_rotation_matrix_z(angle_to_zx_axis)

        # Align rotation vector to y axis
        angle_to_z_axis = math.asin(n_normal.x)
        angle_to_z_axis = (angle_to_z_axis/math.pi) * 180
        to_z_axis =  CgMath3D.get_rotation_matrix_y(angle_to_z_axis)
        
        world_m = CgMath3D.matrix_multiply(to_center, to_zx_plane)
        world_m = CgMath3D.matrix_multiply(world_m, to_z_axis)
        world_m = CgMath3D.matrix_multiply(world_m, from_center)

        for obj in self.__display_file:
            obj.update_world(world_m)