from .coords2D import Coords2d
from .ABCObject import ABCObject
from .cg_math import CgMath

class Curve2D(ABCObject):
    def __init__(self, name: str, point_coords: list[list[float]], color=(0,0,0)) -> None:

        self.__p_coords = []
        for point in point_coords:
            self.__p_coords.append(Coords2d(point[0], point[1]))

        self.__bezier_matrix = [[-1,3,-3,1],
                                [3,-6,3,0],
                                [-3,3,0,0],
                                [1,0,0,0]]

        curve_coords  = self.__get_curve_coords(self.__p_coords, 0.01)

        super().__init__(name, color, curve_coords)



    @property
    def is_closed(self) -> bool:
        return False

    def to_wavefront(self) -> str:
        wavefront_str = (f"{self.name}\n"
                         f"c {self.color[0]} {self.color[1]} {self.color[2]}\n")
        for point in self.__p_coords:
            wavefront_str += f"b {point.x} {point.y}\n"
        return wavefront_str

    def __get_curve_coords(self, coords:list[Coords2d], step:int):
        point_matrix_x = [[coords[0].x], [coords[1].x], [coords[2].x], [coords[3].x]]
        point_matrix_y = [[coords[0].y], [coords[1].y], [coords[2].y], [coords[3].y]]

        curve_coords = self.__add_to_curve(point_matrix_x, point_matrix_y, step)
        i = 3
        while(i < len(coords)-1):
            point_matrix_x = [[coords[i].x], [coords[i+1].x], [coords[i+2].x], [coords[i+3].x]]
            point_matrix_y = [[coords[i].y], [coords[i+1].y], [coords[i+2].y], [coords[i+3].y]]
            curve_coords += self.__add_to_curve(point_matrix_x, point_matrix_y, step)
            i+=3
        return curve_coords


    def __add_to_curve(self, point_matrix_x : list[list[float]], point_matrix_y : list[list[float]], step : int):
        curve_coords = []

        i = 0
        while(i <= 1):
            t = i
            m_t = [[pow(t,3), pow(t,2), t, 1]]

            cx = CgMath.matrix_multiply(self.__bezier_matrix, point_matrix_x)
            cy = CgMath.matrix_multiply(self.__bezier_matrix, point_matrix_y)

            xm = CgMath.matrix_multiply(m_t, cx)
            ym = CgMath.matrix_multiply(m_t, cy)

            curve_coords.append(Coords2d(xm[0][0], ym[0][0]))
            
            i+=step

        return curve_coords


    def update_clipping(self):
        self._clipped_coords = CgMath.shuterland_hodgeman_polygon_clipping(self.normalized_coords, False)

