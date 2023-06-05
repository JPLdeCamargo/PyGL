from .coords3D import Coords3d
from .ABCObject3D import ABCObject3D
from .cg_math_3D import CgMath3D

class Spline3D(ABCObject3D):
    def __init__(self, name: str,  curve_params:list[list[tuple[int]]], color=(0,0,0)) -> None:

        self.__curves_params = curve_params

        self.__b_spline_matrix = [[-1/6, 3/6, -3/6, 1/6],
                                  [3/6, -6/6, 3/6, 0],
                                  [-3/6, 0, 3/6, 0],
                                  [1/6, 4/6, 1/6, 0]]
        
        self.__transposed = CgMath3D.transpose(self.__b_spline_matrix)

        self.__curve_coords, vertices  = self.__get_curve_coords(0.01, 10)

        super().__init__(name, color, vertices)


    def to_wavefront(self) -> str:
        wavefront_str = (f"{self.name}\n"
                         f"c {self.color[0]} {self.color[1]} {self.color[2]}\n")
        for point in self.__curves_params:
            wavefront_str += f"b {point.x} {point.y}\n"
        return wavefront_str

    def __get_curve_coords(self, step:float, n_curves:int):
        curve_coords = []
        vertices = []
        for i in range(0, len(self.__curves_params) - 3):
            for j in range(0, len(self.__curves_params) - 3):
                crt_matrix = [[self.__curves_params[x][y] for y in range(j, j+4)] for x in range(i, i+4)]
                self.__get_subcurve_coords(step, n_curves, crt_matrix, curve_coords, vertices)
        return curve_coords, vertices

    def __get_subcurve_coords(self, step:float, n_curves:int, crt_matrix:list[list[float]],
                              curve_coords:list[int], vertices:list[Coords3d], ):
        curve_param_x = [[j[0] for j in i] for i in crt_matrix]
        curve_param_y = [[j[1] for j in i] for i in crt_matrix]
        curve_param_z = [[j[2] for j in i] for i in crt_matrix]

        cx = CgMath3D.matrix_multiply_multiple(self.__b_spline_matrix, curve_param_x, self.__transposed)
        cy = CgMath3D.matrix_multiply_multiple(self.__b_spline_matrix, curve_param_y, self.__transposed)
        cz = CgMath3D.matrix_multiply_multiple(self.__b_spline_matrix, curve_param_z, self.__transposed)

        big_step = 1/n_curves

        init_small = [[0, 0, 0, 1],
                      [pow(step, 3), pow(step, 2), step, 0],
                      [6*pow(step, 3), 2*pow(step, 2), 0, 0],
                      [6*pow(step, 3), 0, 0, 0]]
        init_big = [[0, 0, 0, 1],
                      [pow(big_step, 3), pow(big_step, 2), big_step, 0],
                      [6*pow(big_step, 3), 2*pow(big_step, 2), 0, 0],
                      [6*pow(big_step, 3), 0, 0, 0]]

        dd1x = CgMath3D.matrix_multiply_multiple(init_big, cx, CgMath3D.transpose(init_small))
        dd1y = CgMath3D.matrix_multiply_multiple(init_big, cy, CgMath3D.transpose(init_small))
        dd1z = CgMath3D.matrix_multiply_multiple(init_big, cz, CgMath3D.transpose(init_small))

        s = 0
        while(s <= 1):
            self.__fwd_diff(step, vertices, curve_coords,
                            dd1x[0][0], dd1x[0][1], dd1x[0][2], dd1x[0][3],
                            dd1y[0][0], dd1y[0][1], dd1y[0][2], dd1y[0][3],
                            dd1z[0][0], dd1z[0][1], dd1z[0][2], dd1z[0][3])
            for i in range(3):
                for j in range(4):
                    dd1x[i][j] += dd1x[i+1][j]
                    dd1y[i][j] += dd1y[i+1][j]
                    dd1z[i][j] += dd1z[i+1][j]

            s += big_step


        dd2x = CgMath3D.transpose(CgMath3D.matrix_multiply_multiple(init_small, cx, CgMath3D.transpose(init_big)))
        dd2y = CgMath3D.transpose(CgMath3D.matrix_multiply_multiple(init_small, cy, CgMath3D.transpose(init_big)))
        dd2z = CgMath3D.transpose(CgMath3D.matrix_multiply_multiple(init_small, cz, CgMath3D.transpose(init_big)))
        t = 0
        while(t <= 1):
            self.__fwd_diff(step, vertices, curve_coords,
                            dd2x[0][0], dd2x[0][1], dd2x[0][2], dd2x[0][3],
                            dd2y[0][0], dd2y[0][1], dd2y[0][2], dd2y[0][3],
                            dd2z[0][0], dd2z[0][1], dd2z[0][2], dd2z[0][3])
            for i in range(3):
                for j in range(4):
                    dd2x[i][j] += dd2x[i+1][j]
                    dd2y[i][j] += dd2y[i+1][j]
                    dd2z[i][j] += dd2z[i+1][j]

            t += big_step

    def __fwd_diff(self, step, vertices, curve_coords,
                   fx, dfx, scnd_dfx, third_dfx,
                   fy, dfy, scnd_dfy, third_dfy,
                   fz, dfz, scnd_dfz, third_dfz):
        new_coords = []
        i = 0
        while(i < 2):
            i += step
            fx, dfx, scnd_dfx = fx + dfx, dfx + scnd_dfx, scnd_dfx + third_dfx
            fy, dfy, scnd_dfy = fy + dfy, dfy + scnd_dfy, scnd_dfy + third_dfy
            fz, dfz, scnd_dfz = fz + dfz, dfz + scnd_dfz, scnd_dfz + third_dfz

            vertices.append(Coords3d(fx, fy, fz))
            new_coords.append(len(vertices)-1)

            i += step


        curve_coords.append(new_coords)


    def update_clipping(self):
        self._clipped_coords = []
        for curve  in self.__curve_coords:
            curve_coords = [self.normalized_coords[i] for i in curve]
            clipped = CgMath3D.shuterland_hodgeman_polygon_clipping(curve_coords, False)
            for i in range(len(clipped)-1):
                self._clipped_coords.append((clipped[i], clipped[i+1]))



