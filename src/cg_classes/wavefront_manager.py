from .game_objects.ABCObject import ABCObject
from .game_objects.line import Line
from .game_objects.point import Point
from .game_objects.wireframe import WireFrame
from ..enums.obj_types import ObjTypes

import os


class WavefrontManager:
    def __init__(self, save_path:str) -> None:
        self.__save_path = save_path

    def save(self, obj:ABCObject, sub_directory:str) -> None:
        path = os.path.join(self.__save_path, sub_directory)
        wavefront_str = obj.to_wavefront()
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        f = open((os.path.join(path, f"{obj.name}.obj")), 'w')
        f.write(wavefront_str)
        f.close()

    def backup_files(self, objs:list[ABCObject]):
        path = os.path.join(self.__save_path, "backup")
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        for obj in objs:
            self.save(obj, "backup")

    def load_all(self) -> list[ABCObject]:
        path = os.path.join(self.__save_path, "load_on_start")
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        to_load = []
        for file_name in os.listdir(path):
            to_load.append(self.load(os.path.join(self.__save_path, "load_on_start", file_name)))
        return to_load
            

    def load(self, path:str) -> ABCObject:
        # Structure:
        # First line = name
        # Second line = color
        # Remaining = points
        # In case of a wireframe, last line = identifier if the polygon is closed or not

        f = open(path)
        wavefront_lines = f.readlines()
        f.close()

        name = wavefront_lines[0][:-1]
        wavefront_lines.pop(0)
        color = [int(i) for i in wavefront_lines[0][2:].split()]
        wavefront_lines.pop(0)

        obj_type = ObjTypes.NONE

            
        is_open = False
        line = wavefront_lines[0]
        if line[0] == 'l':
            obj_type = ObjTypes.LINE
        elif line[0] == 'p':
            obj_type = ObjTypes.POINT
        elif line[0] == 'f':
            obj_type = ObjTypes.WIREFRAME
            id, value  = wavefront_lines[-1].split()
            if value == '1':
                is_open = True
            wavefront_lines.pop(-1)

        coords = []
        for line in wavefront_lines:

            line = line[2:]
            x, y = line.split()
            coords.append((float(x), float(y)))


        if obj_type == ObjTypes.LINE:
            return(Line(name, coords[0], coords[1], color))
        elif obj_type == ObjTypes.POINT:
            return(Point(name, coords[0], color))
        elif obj_type == ObjTypes.WIREFRAME:
            return(WireFrame(name, is_open, coords, color))
            
