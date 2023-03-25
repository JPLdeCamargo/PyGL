import math

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

if __name__ == "__main__":
    a = [[2, 2],
         [3, 3],
         [4, 4]]
    b = [[1, 1, 6, 7, 8],
         [4, 4, 6, 7, 8]]
    print(CgMath.matrix_multiply(a, b))





