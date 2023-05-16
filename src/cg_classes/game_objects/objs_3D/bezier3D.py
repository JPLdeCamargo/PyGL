from .coords3D import Coords3d
from .ABCObject3D import ABCObject3D
from .cg_math_3D import CgMath3D

class Bezier3D(ABCObject3D):
    def __init__(self, name: str,  curve_params:list[list[tuple[int]]], color=(0,0,0)) -> None:

        self.__curves_params = curve_params

        self.__bezier_matrix = [[-1,3,-3,1],
                                [3,-6,3,0],
                                [-3,3,0,0],
                                [1,0,0,0]]

        self.__curve_coords, vertices  = self.__get_curve_coords(0.01, 10)

        super().__init__(name, color, vertices)


    def to_wavefront(self) -> str:
        wavefront_str = (f"{self.name}\n"
                         f"c {self.color[0]} {self.color[1]} {self.color[2]}\n")
        for point in self.__curves_params:
            wavefront_str += f"b {point.x} {point.y}\n"
        return wavefront_str

    def __get_curve_coords(self, step:int, n_curves:int):
        curve_param_x = [[j[0] for j in i] for i in self.__curves_params]
        curve_param_y = [[j[1] for j in i] for i in self.__curves_params]
        curve_param_z = [[j[2] for j in i] for i in self.__curves_params]

        curve_coords = []
        vertices = []
        big_step = 1/n_curves

        mgx = CgMath3D.matrix_multiply(self.__bezier_matrix, curve_param_x)
        mgy = CgMath3D.matrix_multiply(self.__bezier_matrix, curve_param_y)
        mgz = CgMath3D.matrix_multiply(self.__bezier_matrix, curve_param_z)

        mgxm = CgMath3D.matrix_multiply(mgx, self.__bezier_matrix)
        mgym = CgMath3D.matrix_multiply(mgy, self.__bezier_matrix)
        mgzm = CgMath3D.matrix_multiply(mgz, self.__bezier_matrix)

        s = 0
        while(s <= 1):
            crt_curve = []
            m_s = [[pow(s,3), pow(s,2), s, 1]]
            smgxm = CgMath3D.matrix_multiply(m_s, mgxm)
            smgym = CgMath3D.matrix_multiply(m_s, mgym)
            smgzm = CgMath3D.matrix_multiply(m_s, mgzm)

            t = 0
            while(t <= 1):
                m_t = [[pow(t,3)], [pow(t,2)], [t], [1]]

                x = CgMath3D.matrix_multiply(smgxm, m_t)[0][0]
                y = CgMath3D.matrix_multiply(smgym, m_t)[0][0]
                z = CgMath3D.matrix_multiply(smgzm, m_t)[0][0]
            
                vertices.append(Coords3d(x, y, z))
                crt_curve.append(len(vertices)-1)

                t+= step

            s += big_step

            curve_coords.append(crt_curve)

        t = 0
        while(t <= 1):
            crt_curve = []
            m_t = [[pow(t,3)], [pow(t,2)], [t], [1]]
            smgxm = CgMath3D.matrix_multiply(mgxm, m_t)
            smgym = CgMath3D.matrix_multiply(mgym, m_t)
            smgzm = CgMath3D.matrix_multiply(mgzm, m_t)

            s = 0
            while(s <= 1):
                m_s = [[pow(s,3), pow(s,2), s, 1]]

                x = CgMath3D.matrix_multiply(m_s, smgxm)[0][0]
                y = CgMath3D.matrix_multiply(m_s, smgym)[0][0]
                z = CgMath3D.matrix_multiply(m_s, smgzm)[0][0]
            
                vertices.append(Coords3d(x, y, z))
                crt_curve.append(len(vertices)-1)

                s+= step

            t += big_step

            curve_coords.append(crt_curve)

        return curve_coords, vertices
    

    def update_clipping(self):
        self._clipped_coords = []
        for curve  in self.__curve_coords:
            curve_coords = [self.normalized_coords[i] for i in curve]
            clipped = CgMath3D.shuterland_hodgeman_polygon_clipping(curve_coords, False)
            for i in range(len(clipped)-1):
                self._clipped_coords.append((clipped[i], clipped[i+1]))



