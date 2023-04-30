from .coords2D import Coords2d
from .ABCObject import ABCObject
from .cg_math_2D import CgMath2D

class Curve2D(ABCObject):
    def __init__(self, name: str, point_coords: list[list[float]], color=(0,0,0)) -> None:

        self.__p_coords = []
        for point in point_coords:
            self.__p_coords.append(Coords2d(point[0], point[1]))

        self.__bezier_matrix = [[-1,3,-3,1],
                                [3,-6,3,0],
                                [-3,3,0,0],
                                [1,0,0,0]]

        self.__b_spline_matrix = [[-1/6, 3/6, -3/6, 1/6],
                                  [3/6, -6/6, 3/6, 0],
                                  [-3/6, 0, 3/6, 0],
                                  [1/6, 4/6, 1/6, 0]]

        curve_coords  = self.__get_curve_coords_spline(self.__p_coords, 0.01)

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

    # B-spline implementation
    def __get_curve_coords_spline(self, coords:list[Coords2d], step:float):
        cubed = pow(step, 3)
        squared = pow(step, 2)
        done_lines = {} # map for not drawing same lines twice
        curve_coords = []
        # loop create each sub curve
        for i in range(3, len(coords)):
            g_matrix_x = [[coords[i-3].x],[coords[i-2].x], [coords[i-1].x], [coords[i].x]]
            c_matrix_x = CgMath.matrix_multiply(self.__b_spline_matrix, g_matrix_x)

            g_matrix_y = [[coords[i-3].y],[coords[i-2].y], [coords[i-1].y], [coords[i].y]]
            c_matrix_y = CgMath.matrix_multiply(self.__b_spline_matrix, g_matrix_y)

            ax, bx, cx, dx = c_matrix_x[0][0], c_matrix_x[1][0], c_matrix_x[2][0], c_matrix_x[3][0]
            ay, by, cy, dy = c_matrix_y[0][0], c_matrix_y[1][0], c_matrix_y[2][0], c_matrix_y[3][0]

            fx , dfx, scnd_dfx, third_dfx = dx , (ax*cubed + bx*squared + cx*step), (6*ax*cubed + 2*bx*squared), (6*ax*cubed)
            fy , dfy, scnd_dfy, third_dfy = dy , (ay*cubed + by*squared + cy*step), (6*ay*cubed + 2*by*squared), (6*ay*cubed)

            new_coords = self.__fwd_diff(step, done_lines,
                                        fx, dfx, scnd_dfx, third_dfx,
                                        fy, dfy, scnd_dfy, third_dfy)
            curve_coords += new_coords
        return curve_coords

    def __fwd_diff(self, step, done_lines,
                   fx, dfx, scnd_dfx, third_dfx,
                   fy, dfy, scnd_dfy, third_dfy):
        new_coords = []
        old_fx = fx
        old_fy = fy
        i = 0
        while(i < 1):
            i += step
            fx, dfx, scnd_dfx = fx + dfx, dfx + scnd_dfx, scnd_dfx + third_dfx
            fy, dfy, scnd_dfy = fy + dfy, dfy + scnd_dfy, scnd_dfy + third_dfy

            if(not (old_fx, old_fy, fx, fy) in done_lines):
                done_lines[(old_fx, old_fy, fx, fy)] = True
                new_coords.append(Coords2d(fx, fy))

            old_fx = fx
            old_fy = fy

        return new_coords

    # Bezier implementation
    def __get_curve_coords_bezier(self, coords:list[Coords2d], step:float):
        point_matrix_x = [[coords[0].x], [coords[1].x], [coords[2].x], [coords[3].x]]
        point_matrix_y = [[coords[0].y], [coords[1].y], [coords[2].y], [coords[3].y]]

        curve_coords = self.__add_to_curve_bezier(point_matrix_x, point_matrix_y, step)
        i = 3
        while(i < len(coords)-1):
            point_matrix_x = [[coords[i].x], [coords[i+1].x], [coords[i+2].x], [coords[i+3].x]]
            point_matrix_y = [[coords[i].y], [coords[i+1].y], [coords[i+2].y], [coords[i+3].y]]
            curve_coords += self.__add_to_curve_bezier(point_matrix_x, point_matrix_y, step)
            i+=3
        return curve_coords


    def __add_to_curve_bezier(self, point_matrix_x : list[list[float]], point_matrix_y : list[list[float]], step : int):
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

