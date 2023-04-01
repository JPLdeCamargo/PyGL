from abc import ABC, abstractmethod
from .coords2D import Coords2d
from .cg_math import CgMath

class ABCObject(ABC):
    def __init__(self, name: str, color : tuple[int], coords: list[Coords2d]) -> None:
        super().__init__()
        self.__name = name
        self.__color = color
        self.__coords = coords
        self.__normalized_coords = []

    @property
    def coords(self) -> list[Coords2d]:
        return self.__coords

    @property
    def normalized_coords(self) -> list[Coords2d]:
        return self.__normalized_coords

    @property
    @abstractmethod
    def is_closed(self) -> bool:
        pass

    @property
    def name(self) -> str:
        return self.__name

    @property
    def color(self) -> tuple[int]:
        return self.__color

    def update_normalized(self, normalized_m:list[list[float]]):
        self.__normalized_coords = []
        for point in self.coords:
            homogenous = [[point.x, point.y, 1]]
            transformed = CgMath.matrix_multiply(homogenous, normalized_m)
            x = transformed[0][0]
            y = transformed[0][1]
            self.__normalized_coords.append(Coords2d(x, y))

    
    def rotate(self, degree_angle : float, anchor : Coords2d):
        matrix = self.__get_center_rotation_matrix(anchor, degree_angle)

        self.__apply_matrix_transform(matrix)

    def scale(self, vx, vy):
        center = self.get_center()
        matrix = self.__get_center_scale_matrix(center, vx, vy)

        self.__apply_matrix_transform(matrix)

    def translate(self, vx, vy):
        matrix = CgMath.get_translation_matrix(vx, vy)

        self.__apply_matrix_transform(matrix)

    def __apply_matrix_transform(self, matrix :list[list[int]]):
        for i in range(len(self.__coords)):
            point = self.__coords[i]

            homogenous = [[point.x, point.y, 1]]
            transformed = CgMath.matrix_multiply(homogenous, matrix)
            self.__coords[i].x = transformed[0][0]
            self.__coords[i].y = transformed[0][1]

            if len(self.__normalized_coords) != 0:
                norm_point = self.__normalized_coords[i]

                homogenous = [[norm_point.x, norm_point.y, 1]]
                transformed = CgMath.matrix_multiply(homogenous, matrix)
                norm_point.x = transformed[0][0]
                self.__normalized_coords[i].x = transformed[0][0]
                self.__normalized_coords[i].y = transformed[0][1]



    def __get_center_rotation_matrix(self, center: Coords2d, degree_angle : float):
        to_center_matrix = CgMath.get_translation_matrix(-center.x, -center.y)
        rotation_matrix = CgMath.get_rotation_matrix(degree_angle)
        from_center_matrix = CgMath.get_translation_matrix(center.x, center.y)

        aux = CgMath.matrix_multiply(to_center_matrix, rotation_matrix)
        return CgMath.matrix_multiply(aux, from_center_matrix)

    def __get_center_scale_matrix(self, center : Coords2d, vx : float, vy : float):
        to_center_matrix = CgMath.get_translation_matrix(-center.x, -center.y)
        scale_matrix = CgMath.get_scale_matrix(vx, vy)
        from_center_matrix = CgMath.get_translation_matrix(center.x, center.y)

        aux = CgMath.matrix_multiply(to_center_matrix, scale_matrix)
        return CgMath.matrix_multiply(aux, from_center_matrix)

    def get_center(self):
        center = Coords2d(0, 0)
        for point in self.coords:
            center.x += point.x
            center.y += point.y
        center.x /= len(self.coords)
        center.y /= len(self.coords)
        return center 

