from .game_objects.objs_2D.coords2D import Coords2d
from .game_objects.objs_3D.coords3D import Coords3d
from .game_objects.objs_3D.ABCObject3D import ABCObject3D
from .phong_equations import PhongModel

import math
import copy


class Rasterizer:
    def __init__(self, viewport_size: Coords2d, viewport_offset: Coords2d) -> None:
        self.__viewport_size = viewport_size
        self.__viewport_offset = viewport_offset



    def __transform_to_viewport(self, point:Coords3d) -> Coords3d:
        boundary_coord = Coords2d(self.__viewport_size.x - self.__viewport_offset.x * 2,
                                  self.__viewport_size.y - self.__viewport_offset.y * 2)
        unit = self.__transform_into_unitary(point)
        transformed = unit * boundary_coord
        # Adding offset
        transformed.x += self.__viewport_offset.x
        transformed.y += self.__viewport_offset.y
        transformed = Coords3d(transformed.x, transformed.y, point.z)
        return transformed

    def __transform_into_unitary(self, point:Coords3d) -> Coords2d:
        unit_x = (point.x + 1)/2
        unit_y = 1 - ((point.y + 1)/2)
        return Coords2d(unit_x, unit_y)

    def rasterize_obj(self, obj:ABCObject3D, window_center:Coords3d, light_loc:Coords3d):
        rast_res = {}
        print("center")
        print(window_center)
        coords = obj.rasterizer_coords
        for face in coords:
            v_coords = [self.__transform_to_viewport(i) for i in face]
            if len(v_coords)<=2:
                continue
            v_coords.pop(-1)
            # Remove equals
            done = {}
            i = 0
            while True:
                crt = (round(v_coords[i].x,5), round(v_coords[i].y,5))
                if crt in done:
                    del v_coords[i]
                else:
                    done[crt] = True
                    i+=1
                if i >= len(v_coords):
                    break;

            if len(v_coords) < 3:
                continue
            
            shaded_color = PhongModel.phong_get_color(v_coords, light_loc, window_center, obj.color)

            traps = self.__get_trapeziums(v_coords)
            for trap in traps:
                self.rasterize_trapezium(rast_res, trap, shaded_color)
        return rast_res

    def rasterize_trapezium(self, rast_res, trap:list[Coords3d], shaded_color:list[int]):
        if len(trap) == 3:
            if round(trap[0].y,4) == round(trap[1].y,4):
                border_1 = [trap[0], trap[2]]
                border_2 = [trap[1], trap[2]]
            else:
                border_1 = [trap[0], trap[1]]
                border_2 = [trap[0], trap[2]]
        else:
            border_1 = [trap[0], trap[-2]]
            border_2 = [trap[1], trap[-1]]

        borders = [border_1, border_2]
        if border_1[0].y == border_1[1].y or border_2[0].y == border_2[1].y:
            return
        pixel_borders = []
        for border in borders:
            pixel_border =[]
            x2, y2, z2 = border[1].x, border[1].y, border[1].z
            x1, y1, z1 = border[0].x, border[0].y, border[0].z
            xd = ((x2-x1)/(y2-y1))
            zd = ((z2-z1)/(y2-y1))
            crt_point = Coords3d(x2+xd, math.floor(y2), z2+zd)
            for i in range(math.floor(y2), math.ceil(y1), -1):
                pixel_x = math.floor(crt_point.x)
                pixel_coord = Coords3d(pixel_x, crt_point.y, crt_point.z)
                pixel_border.append(pixel_coord)
                crt_point.x -= xd
                crt_point.y -= 1
                crt_point.z -= zd

            pixel_borders.append(pixel_border)
        
        for i in range(len(pixel_borders[0])):
            x2, y2, z2 = pixel_borders[1][i].x, pixel_borders[1][i].y, pixel_borders[1][i].z
            x1, y1, z1 = pixel_borders[0][i].x, pixel_borders[0][i].y, pixel_borders[0][i].z
            if x1 == x2:
                continue
            zd = ((z2-z1)/(x2-x1))
            crt_z = z1
            increment = 1 if x1 < x2 else -1
            x2 += increment
            for j in range(x1, x2, increment):
                self.paint(rast_res, Coords3d(j, y1, crt_z), shaded_color) 
                crt_z += zd




    def paint(self, rast_res, point:Coords3d, shaded_color:list[int]):
        if (point.x, point.y) in rast_res:
            if(point.z < rast_res[(point.x, point.y)][0]):
                rast_res[(point.x, point.y)] = (point.z, shaded_color)
        else:
            rast_res[(point.x, point.y)] = (point.z, shaded_color)

                



    def __get_trapeziums(self, face:list[Coords3d]):
        traps = []

        ordered_faces = [(face[i], i) for i in range(len(face))]
        ordered_faces.sort(key=lambda x:(x[0].y ,x[0].x))
        if len(ordered_faces) < 3:
            return []
        to_pass = False
        crt_trap = [ordered_faces[0]]
        if ordered_faces[0][0].y == ordered_faces[1][0].y:
            to_pass = True
            crt_trap.append(ordered_faces[1])
            
        for i in range(1, len(face)-1):
            if to_pass:
                to_pass = False
                continue

            if ordered_faces[i][0].y == ordered_faces[i+1][0].y:
                crt_trap.append(ordered_faces[i])
                crt_trap.append(ordered_faces[i+1])
                to_pass = True

            else:
                crt = ordered_faces[i][0]
                new_coord = self.__get_intercept_y(crt.y, crt.x, face)
                if new_coord is None:
                    print("OH NO")
                    return []
                new_pnts = [ordered_faces[i], (new_coord,ordered_faces[i][1])]
                new_pnts.sort(key=lambda x:x[0].x)
                crt_trap += new_pnts


            to_append = [i[0] for i in crt_trap]
            traps.append(to_append)
            crt_trap.pop(0)
            if(i > 1):
                crt_trap.pop(0)

        if ordered_faces[-1][0].y != ordered_faces[-2][0].y:
            crt_trap.append(ordered_faces[-1])
            to_append = [i[0] for i in crt_trap]
            traps.append(to_append)

        return traps

    def __get_intercept_y(self, y, x, face):
        face_copy = copy.deepcopy(face)
        face_copy.append(face_copy[0])
        for i in range(len(face_copy)-1):
            line = [face_copy[i], face_copy[i+1]]
            intercept = self.__get_new_coord(y, line)
            if not intercept is None and round(x,5) != round(intercept.x, 5):
                return intercept


            

    def __get_new_coord(self, y:float, line:list[Coords3d]) -> Coords3d:
        a, b = line[0], line[1]
        if(round(a.y,5) == round(b.y,5)):
            return
        ax = (b.x - a.x)/(b.y - a.y)
        bx = a.x - (ax * a.y)
        new_x = y * ax + bx

        az = (b.z - a.z)/(b.y - a.y)
        bz = a.z - (az * a.y)
        new_z = y * az + bz
        coord = Coords3d(new_x, y, new_z) 
        mn, mx = sorted([a.x, b.x])
        if(coord.x >= mn and coord.x <= mx):
            return coord


        


