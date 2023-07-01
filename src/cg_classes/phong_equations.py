import numpy as np
import math
from .game_objects.objs_3D.cg_math_3D import Coords3d

class PhongModel:
    
    @staticmethod
    def phong_get_color(face:list[Coords3d], light_location:Coords3d,
                        obser_location:Coords3d, color:list[int]):
        center_x = sum([i.x for i in face])/len(face)
        center_y = sum([i.y for i in face])/len(face)
        center_z = sum([i.z for i in face])/len(face)

        light_dir = np.array([light_location.x - center_x, light_location.y - center_y, light_location.z - center_z])
        nor = abs(np.linalg.norm(light_dir))
        norm_light = light_dir
        if nor != 0:
            norm_light = light_dir / nor

        obser_dir = np.array([obser_location.x - center_x, obser_location.y - center_y, obser_location.z - center_z])
        nor = np.linalg.norm(obser_dir)
        norm_obser = obser_dir
        if nor != 0:
            norm_obser = obser_dir / nor

        vec1 = np.array([face[1].x - face [0].x, face[1].y - face [0].y, face[1].z - face [0].z])
        vec2 = np.array([face[2].x - face [0].x, face[2].y - face [0].y, face[2].z - face [0].z])
        normal_surf = np.cross(vec1, vec2)
        normal_surf = normal_surf / np.linalg.norm(normal_surf)

        # Calculating phong model
        i_dif = PhongModel.__difuse(normal_surf, norm_light)

        difuse_color = (color[0]*i_dif, color[1]*i_dif, color[2]*i_dif)

        i_espc = PhongModel.__especular(norm_obser, norm_light)

        especular_color = tuple([255 * i_espc] * 3)

        i_amb = PhongModel.__ambient()

        amb_color = (color[0]*i_amb, color[1]*i_amb, color[2]*i_amb)

        color_sum = [difuse_color[i] + especular_color[i] + (amb_color[i]*0.1) for i in range(3)]

        for i in range(3):
            if color_sum[i] > 255:
                color_sum[i] = 255


        return color_sum


    @staticmethod
    def __difuse(normal_surf:np.ndarray, norm_light:np.ndarray):
        i_dif = 1 * 1 * np.dot(normal_surf, norm_light)
        return i_dif

    @staticmethod
    def __especular(norm_obs:np.ndarray, norm_light:np.ndarray):
        i_dif = 3 * 1 * pow(np.dot(norm_light, norm_obs),100)
        return i_dif

    @staticmethod
    def __ambient():
        return 1 * 0.5
