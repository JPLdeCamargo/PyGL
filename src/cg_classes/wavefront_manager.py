from .game_objects.objs_3D.ABCObject3D import ABCObject3D
# from .game_objects.line import Line
from .game_objects.objs_3D.point3D import Point3D
from .game_objects.objs_3D.wireframe3D import WireFrame3D
# from .game_objects.curve2D import Curve2D
from ..enums.obj_types import ObjTypes

import os


class WavefrontManager:
    def __init__(self, save_path:str) -> None:
        self.__save_path = save_path

    def save(self, obj:ABCObject3D, sub_directory:str) -> None:
        path = os.path.join(self.__save_path, sub_directory)
        wavefront_str = obj.to_wavefront()
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        f = open((os.path.join(path, f"{obj.name}.obj")), 'w')
        f.write(wavefront_str)
        f.close()

    def backup_files(self, objs:list[ABCObject3D]):
        path = os.path.join(self.__save_path, "backup")
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        for obj in objs:
            self.save(obj, "backup")

    def load_all(self) -> list[ABCObject3D]:
        path = os.path.join(self.__save_path, "load_on_start")
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        to_load = []
        for file_name in os.listdir(path):
            to_load.append(self.load_wireframe3D(os.path.join(self.__save_path, "load_on_start", file_name)))
        return to_load
            

    def load_wireframe3D(self, path:str) -> ABCObject3D:
        f = open(path)
        wavefront_lines = f.readlines()
        f.close()

        name = wavefront_lines[0]
        name = name[:-1]
        wavefront_lines = wavefront_lines[1:]

        coords = []
        faces = []
        for line in wavefront_lines:

            if line[:2] == "v ":
                _, x, y, z = line.split()
                new_coord = (float(x), float(y), float(z))
                coords.append(new_coord)
            if line[:2] == "f ":
                l = line[2:]
                face = tuple([int(i.split("/")[0])-1 for i in (l.split())])
                faces.append(face)
        
        return WireFrame3D(name, faces, coords)
                    

