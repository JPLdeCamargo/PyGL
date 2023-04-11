import math
from .coords2D import Coords2d

class CgMath:

    @staticmethod
    def matrix_multiply(a : list[list[float]], b: list[list[float]]):
        result = []
        for i in range(len(a)):
            row = []
            for j in range(len(b[0])):
                sum = 0
                for x in range(len(a[0])):
                    sum += a[i][x] * b[x][j]
                row.append(sum)
            result.append(row)
        return result

    @staticmethod
    def get_translation_matrix(vx: float, vy:float):
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [vx, vy, 1]]
        return translation_matrix

    @staticmethod
    def get_scale_matrix(vx: float, vy:float):
        scale_matrix = [[vx, 0, 0],
                        [0, vy, 0],
                        [0, 0, 1]]
        return scale_matrix

    @staticmethod
    def get_rotation_matrix(vx: float, vy:float):
        scale_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [vx, vy, 1]]
        return scale_matrix

    @staticmethod
    def get_rotation_matrix(degree_angle : float):
        rad = math.radians(degree_angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        rotation_matrix = [[cos, -sin, 0],
                        [sin, cos, 0],
                        [0, 0, 1]]
        return rotation_matrix


    @staticmethod
    def __is_trespassing(a:Coords2d, flag_in_question:int):
        codes_a = CgMath.__get_clipping_codes(a)
        if codes_a[flag_in_question]:
            return True
        return False

    @staticmethod
    def shuterland_hodgeman_polygon_clipping(coords:list[Coords2d], closed=True) -> list[Coords2d]:
        crt_poly = coords
        if closed:
            crt_poly.append(crt_poly[0])
        for i in range(4):
            flags = [False] * 4
            crt_flag = flags
            crt_flag[i] = True
            # crt_flag = [False, True, False, False]
            new_poly = []
            outside = True
            for j in range(0, len(crt_poly) - 1):
                a = crt_poly[j]
                b = crt_poly[j +1]
                if(CgMath.__is_trespassing(a, i)):
                    outside = True
                new_point = CgMath.cohen_shuterland_line_clipping(a, b, crt_flag)

                if len(new_point) == 0:
                    outside = True
                if len(new_point) == 2:
                    if outside:
                        outside = False
                        new_poly += new_point
                    else:
                        new_poly.append(new_point[1])

            crt_poly = new_poly
            if closed and len(crt_poly) > 0:
                crt_poly.append(crt_poly[0])
        return crt_poly[:-1]
                




    # Flags added for Shuterland polygon clipping
    # disabling a flag disables clipping on that specific limit
    @staticmethod
    def cohen_shuterland_line_clipping(a: Coords2d, b : Coords2d, flags=[True, True, True, True]) -> list[Coords2d]:
        codes_a = CgMath.__get_clipping_codes(a)
        codes_b = CgMath.__get_clipping_codes(b)

        codes_a = [a and f for a, f in zip(codes_a, flags)]
        codes_b = [b and f for b, f in zip(codes_b, flags)]

        if codes_a == codes_b == [False, False, False, False]: # Completely contained
            return [a, b]
        elif [a and b for a, b in zip(codes_a, codes_b)] != [False, False, False, False]: # Completely outside
            return []
        else: # Partially contained
            angle_coef = (b.y - a.y)/(b.x - a.x + 0.00001)
            new_a = CgMath.__get_clip_coords(angle_coef, a, codes_a, flags)
            new_b = CgMath.__get_clip_coords(angle_coef, b, codes_b, flags)

            return [new_a, new_b]
            

    @staticmethod
    def __get_clip_coords(m, a, codes_a, flags:list[bool]):
        active_flags = 0
        for flag in flags:
            if flag:
                active_flags += 1

        for i in range(len(codes_a)):
            if codes_a[i]:
                if i == 0 and flags[0]: # Top
                    y = 1
                    x = a.x + 1/m * (1 - a.y)
                    if(active_flags <= 1 or (x >= -1 and x <= 1)):
                        return Coords2d(x, y)
                elif i == 1 and flags[1]: # Bottom
                    y = -1
                    x = a.x + 1/m * (-1 - a.y)
                    if(active_flags <= 1 or (x >= -1 and x <= 1)):
                        return Coords2d(x, y)
                elif i == 2 and flags[2]: # Right
                    y = m * (1 - a.x) + a.y
                    x = 1
                    if(active_flags <= 1 or (y >= -1 and y <= 1)):
                        return Coords2d(x, y)
                elif i == 3 and flags[3]: # Left
                    y = m * (-1 - a.x) + a.y
                    x = -1
                    if(active_flags <= 1 or (y >= -1 and y <= 1)):
                        return Coords2d(x, y)
        return a

    @staticmethod
    def __get_clipping_codes(point:Coords2d) -> list[bool]:
        first = True if point.y > 1 else False # Top
        second = True if point.y < -1 else False # Bottom
        third = True if point.x > 1 else False # Right
        forth = True if point.x < -1 else False # Left
        return [first, second, third, forth] 


if __name__ == "__main__":
    a = [[2, 2],
         [3, 3],
         [4, 4]]
    b = [[1, 1, 6, 7, 8],
         [4, 4, 6, 7, 8]]
    print(CgMath.matrix_multiply(a, b))





