import math
from abc import ABC, abstractmethod
from .coords3D import Coords3d
from .cg_math_3D import CgMath3D

from ..objs_2D.cg_math_2D import CgMath2D
from ..objs_2D.coords2D import Coords2d

class ABCObject3D(ABC):
    def __init__(self, name: str, color : tuple[int], vertices: list[Coords3d]) -> None:
        super().__init__()
        self.__name = name
        self.__color = color
        self.__coords = vertices
        self.__world_coords = []
        # Window coordinates
        self.__normalized_coords = []

        self._clipped_coords = []
        self._rasterizer_coords = []

        # Used for calculating normalized coordinates after transformations
        self.__last_normalized_m = None
        self.__last_world_m = None

    @property
    def coords(self) -> list[Coords3d]:
        return self.__coords

    @property
    def normalized_coords(self) -> list[Coords3d]:
        return self.__normalized_coords

    @property
    def rasterizer_coords(self) -> list[Coords3d]:
        return self._rasterizer_coords

    @property
    def clipped_coords(self) -> list[Coords3d]:
        return self._clipped_coords

    @property
    def name(self) -> str:
        return self.__name

    @property
    def color(self) -> tuple[int]:
        return self.__color

    @abstractmethod
    def to_wavefront(self) -> str:
        pass
    
    @abstractmethod
    def update_clipping(self):
        pass


    def update_normalized(self, normalized_m:list[list[float]]):
        self.__normalized_coords = []
        self.__last_normalized_m = normalized_m
        for point in self.__world_coords:
            homogenous = [[point.x, point.y, 1]]
            transformed = CgMath2D.matrix_multiply(homogenous, normalized_m)
            x = transformed[0][0]
            y = transformed[0][1]
            z = point.z
            self.__normalized_coords.append(Coords3d(x, y, z))
        
        self.update_clipping()

    def update_world(self, world_m:list[list[float]]):
        self.__world_coords = []
        self.__last_world_m = world_m
        for point in self.coords:
            homogenous = [[point.x, point.y, point.z, 1]]
            transformed = CgMath2D.matrix_multiply(homogenous, world_m)
            x = transformed[0][0]/transformed[0][3]
            y = transformed[0][1]/transformed[0][3]
            z = transformed[0][2]

            self.__world_coords.append(Coords3d(x, y, z))

    def rotate(self, degree_angle : float, anchor : Coords3d, rotation_vector:Coords3d):
        self.__normalize(rotation_vector)
        matrix = self.__get_center_rotation_matrix(anchor, degree_angle, rotation_vector)

        self.__apply_matrix_transform(matrix)

    def __normalize(self, point:Coords3d):
        d = math.sqrt(pow(point.x, 2) + pow(point.y, 2) + pow(point.z, 2))
        point.x /= d
        point.y /= d
        point.z /= d

    def scale(self, vx, vy, vz):
        center = self.get_center()
        matrix = self.__get_center_scale_matrix(center, vx, vy, vz)

        self.__apply_matrix_transform(matrix)

    def translate(self, vx, vy, vz):
        matrix = CgMath3D.get_translation_matrix(vx, vy, vz)

        self.__apply_matrix_transform(matrix)

    def __apply_matrix_transform(self, matrix :list[list[int]]):
        for i in range(len(self.__coords)):
            point = self.__coords[i]

            homogenous = [[point.x, point.y, point.z, 1]]
            transformed = CgMath3D.matrix_multiply(homogenous, matrix)
            self.__coords[i].x = transformed[0][0]
            self.__coords[i].y = transformed[0][1]
            self.__coords[i].z = transformed[0][2]

        if len(self.__normalized_coords) != 0:
            self.update_world(self.__last_world_m)
            self.update_normalized(self.__last_normalized_m)

    def __get_center_rotation_matrix(self, center: Coords3d, degree_angle : float, rotation_vector:Coords3d):
        to_center_matrix = CgMath3D.get_translation_matrix(-center.x, -center.y, -center.z)

        # Align rotation vector to xy plane
        angle_to_x_axis = math.asin(rotation_vector.z)
        angle_to_x_axis = (angle_to_x_axis/math.pi) * 180
        to_xy_plane =  CgMath3D.get_rotation_matrix_x(angle_to_x_axis)

        # Align rotation vector to y axis
        angle_to_y_axis = math.asin(rotation_vector.x)
        angle_to_y_axis = (angle_to_y_axis/math.pi) * 180
        to_y_axis =  CgMath3D.get_rotation_matrix_z(angle_to_y_axis)

        #Rotate the desired angle
        actual_rotation = CgMath3D.get_rotation_matrix_y(degree_angle)

        # Redo previous transformations
        redo_y =  CgMath3D.get_rotation_matrix_z(-angle_to_y_axis)
        redo_xy =  CgMath3D.get_rotation_matrix_x(-angle_to_x_axis)
        from_center = CgMath3D.get_translation_matrix(center.x, center.y, center.z)

        aux = CgMath3D.matrix_multiply(to_center_matrix, to_xy_plane)
        aux = CgMath3D.matrix_multiply(aux, to_y_axis)
        aux = CgMath3D.matrix_multiply(aux, actual_rotation)
        aux = CgMath3D.matrix_multiply(aux, redo_y)
        aux = CgMath3D.matrix_multiply(aux, redo_xy)
        aux = CgMath3D.matrix_multiply(aux, from_center)
        return aux

    def __get_center_scale_matrix(self, center : Coords3d, vx : float, vy : float, vz:float):
        to_center_matrix = CgMath3D.get_translation_matrix(-center.x, -center.y, -center.z)
        scale_matrix = CgMath3D.get_scale_matrix(vx, vy, vz)
        from_center_matrix = CgMath3D.get_translation_matrix(center.x, center.y, center.z)

        aux = CgMath3D.matrix_multiply(to_center_matrix, scale_matrix)
        return CgMath3D.matrix_multiply(aux, from_center_matrix)

    def get_center(self):
        center = Coords3d(0, 0, 0)
        for point in self.coords:
            center.x += point.x
            center.y += point.y
            center.z += point.z
        center.x /= len(self.coords)
        center.y /= len(self.coords)
        center.z /= len(self.coords)
        return center 

