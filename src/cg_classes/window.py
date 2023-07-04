from .game_objects.objs_3D.ABCObject3D import ABCObject3D
from .game_objects.objs_3D.coords3D import Coords3d
from .game_objects.objs_3D.cg_math_3D import CgMath3D

from .game_objects.objs_2D.coords2D import Coords2d
from .game_objects.objs_2D.cg_math_2D import CgMath2D

from .game_objects.objs_3D.spline3D import Spline3D
from .game_objects.objs_3D.wireframe3D import WireFrame3D

import math
import copy


class Window:
    def __init__(self, x_size : float, y_size : float, to_load:list[ABCObject3D]) -> None:
        # curve = Spline3D("Terrain",
        #                  [[(2000, 0, 500), (3000, 0 , 500), (4000, 0, 500), (5000, 0, 500),(2000, 4000, 500)],
        #                   [(2000, 0, 1000), (3000, 3000 , 1000), (4000, 2000, 1000), (5000, 0, 1000), (2000, 4000, 1000)],
        #                   [(2000, 0, 1500), (3000, 3000 , 1500), (4000, 2000, 1500), (5000, 0, 1500), (2000, 4000, 1500) ],
        #                   [(2000, 0, 2000), (3000, 3000 , 2000), (4000, 2000, 2000), (5000, 0, 2000), (2000, 4000, 2000) ],
        #                   [(1000, 0, 2500), (7000, 0 , 1000), (3000, 0, 2500), (5000, 0, 2500), (2500, 4000, 2500)]])

        # self.__display_file = [curve]
        self.__display_file = to_load
        # self.__display_file = [WireFrame3D("Lindo",
        #                                         [(0,1,2,3),(4,5,6,7),(1,2,6,5),(0,3,7,4),(3,2,6,7),(0,1,5,4)], 
        #                                         [(0,0,0),(3500,0,0),(3500,0,3500),(0,0,3500),
        #                                             (0,3500,0),(3500,3500,0),(3500,3500,3500),(0,3500,3500)])]
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

        self.__d = max(x_size, y_size)
        self.__perspective_matrix = [[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 1/self.__d],
                                     [0, 0, 0, 0]]

        # Filling normalized coords of all objects
        self.light_loc = Coords3d(7000,7000,0)
        self.update_world()
        self.update_normalized()

    @property
    def distance(self) -> float:
        return self.__d
        
    @property
    def display_file(self) -> list[ABCObject3D]:
        return self.__display_file

    @property
    def up_vector(self) -> Coords3d:
        return self.__up_vector

    @property
    def right_vector(self) -> Coords3d:
        return self.__right_vector

    @property
    def front_vector(self) -> Coords3d:
        return self.__front_vector

    @property
    def center(self) -> Coords3d:
        return self.__center

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

    # def zoom(self, delta:float) -> None:
    #     scale = self.__size.x
    #     delta = (delta * scale)/1000

    #     dx = delta * self.__ratio
    #     dy = delta

    #     self.__size.x += dx 
    #     self.__size.y += dy

    #     self.update_world()
    #     self.update_normalized()
    def zoom(self, delta:float):
        scale = self.__d
        delta = (delta * scale)/1000
        delta_vector = Coords3d(self.__front_vector.x * delta,
                                self.__front_vector.y * delta,
                                self.__front_vector.z * delta)
        self.__center += delta_vector
        print(self.__center)

        self.update_world()
        self.update_normalized()

    def rotate(self, angle:float, rotation_vector:Coords3d):
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
        
        # self.__up_vector = self.__transform_vector(self.__up_vector, rotation_m)
        # self.__right_vector = self.__transform_vector(self.__right_vector, rotation_m)
        # self.__front_vector = self.__transform_vector(self.__front_vector, rotation_m)
        self.light_loc = self.__transform_vector(self.light_loc, rotation_m)

        self.update_world()
        self.update_normalized()

    def __transform_vector(self, x:Coords3d, matrix):
        v = copy.deepcopy(x)
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
        # translate_center_m = CgMath2D.get_translation_matrix(self.__center.x, self.__center.y)

        # Normalizing -1, 1
        scale_x = 2/self.__size.x
        scale_y = 2/self.__size.y
        scale_m = CgMath2D.get_scale_matrix(scale_x, scale_y)
        # translate_m = CgMath2D.get_translation_matrix(-1, -1)
        # normalization_m = CgMath2D.matrix_multiply(scale_m, translate_m)

        # full_normalize_transform = CgMath2D.matrix_multiply(translate_center_m, scale_m)

        for obj in self.__display_file:
            obj.update_normalized(scale_m)

    def update_world(self):
        # to_center = CgMath3D.get_translation_matrix(-self.__center.x, -self.__center.y, -self.__center.z)
        to_cop = CgMath3D.get_translation_matrix(-self.__center.x, -self.__center.y, -(self.__center.z - self.__d))

        # Align rotation vector to zx plane
        angle_to_zy_axis = self.__get_angle(Coords2d(0,1), Coords2d(self.__front_vector.x, self.__front_vector.z))

        angle_to_z_axis = -self.__get_angle(Coords2d(0, 1), Coords2d(self.__front_vector.y, self.__front_vector.z))
        if self.__front_vector.z < 0.01:
            angle_to_z_axis *= -1
        
        # Align right to xy plane
        angle_right_xy_plane = self.__get_angle(Coords2d(0,1), Coords2d(self.__right_vector.y, self.__right_vector.x))

        to_zy_plane =  CgMath3D.get_rotation_matrix_y(-angle_to_zy_axis)

        to_z_axis =  CgMath3D.get_rotation_matrix_x(-angle_to_z_axis)

        r_to_xy = CgMath3D.get_rotation_matrix_z(-angle_right_xy_plane)


        
        test = CgMath3D.matrix_multiply(to_zy_plane, to_z_axis)
        test = CgMath3D.matrix_multiply(test, r_to_xy)

        v_up = self.__transform_vector(self.__up_vector, test)
        v_front = self.__transform_vector(self.__front_vector, test)
        v_right = self.__transform_vector(self.__right_vector, test)

        # all axis are aligned, but are negative
        if abs(v_front.z - 1) > 0.01:
            if abs(v_up.y-1) < 0.01:
                re_arrange = CgMath3D.get_rotation_matrix_y(180)
            else:
                re_arrange = CgMath3D.get_rotation_matrix_x(180)
            test = CgMath3D.matrix_multiply(test, re_arrange)

        # debugging purposes
        # v_up = self.__transform_vector(self.__up_vector, test)
        # v_front = self.__transform_vector(self.__front_vector, test)
        # v_right = self.__transform_vector(self.__right_vector, test)
        # print("_____________________________________________________________")
        # print(v_up, v_front, v_right)

        world_m = CgMath3D.matrix_multiply(to_cop, test)

        world_m = CgMath3D.matrix_multiply(world_m, self.__perspective_matrix)


        for obj in self.__display_file:
            obj.update_world(world_m)

    # a vector already is an axis        
    def __get_angle(self, a:Coords2d, b:Coords2d):
        bs = math.sqrt(math.pow(b.x, 2) + math.pow(b.y,2))
        if abs(bs) < 0.01:
            return 0

        angle = math.acos(((a.x * b.x) + (a.y *b.y)) / bs)

        angle = (angle/math.pi) * 180

        if b.x < 0 and abs(b.x) > 0.01:
            angle *= -1

        return angle