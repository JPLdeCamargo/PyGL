from .window import Window
from .game_objects.coords2D import Coords2d
from .game_objects.ABCObject import ABCObject

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

import math

class Viewport(QWidget):
    def __init__(self, max_x:int, max_y:int, window:Window) -> None:
        super().__init__()

        self.__max_x = max_x
        self.__max_y = max_y
        self.__min_x = 0
        self.__min_y = 0

        # New set of boundary coords for clipping test
        self.__offset = Coords2d(50, 50)


        self.__window = window

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('grey'))
        self.setPalette(palette)

    # Return a tuple, first = coords list, second = colors list
    def world_to_screen_coords(self):
        viewport_objs = []
        colors = []
        world_objs_coords = self.__window.display_file
        for obj in world_objs_coords:

            # Transforming normalized coords into viewport coords
            viewport_coords = []
            colors.append(obj.color)
            for coord in obj.clipped_coords:
                transformed = self.__transform_to_viewport(coord)
                viewport_coords.append(transformed)

            if obj.is_closed and len(obj.clipped_coords) > 0:
                transformed = self.__transform_to_viewport(obj.clipped_coords[0])
                viewport_coords.append(transformed)


            viewport_objs.append(viewport_coords)
        return (viewport_objs, colors)
            

    def __transform_to_viewport(self, point:Coords2d) -> Coords2d:
        boundary_coord = Coords2d(self.__max_x - self.__offset.x * 2, self.__max_y - self.__offset.y * 2)
        unit = self.__transform_into_unitary(point)
        transformed = unit * boundary_coord
        # Adding offset
        transformed += self.__offset 
        transformed = Coords2d(math.floor(transformed.x), math.floor(transformed.y))
        return transformed

                 
    # Unitary values to where the point will be
    # relatively to its position on the window coordinates
    def __transform_into_unitary(self, point:Coords2d) -> Coords2d:
        unit_x = (point.x + 1)/2
        unit_y = 1 - ((point.y + 1)/2)
        return Coords2d(unit_x, unit_y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)

        objs = self.world_to_screen_coords()
        for i in range(len(objs[0])):
            obj = objs[0][i]
            color = objs[1][i]
            painter.setPen(QColor(color[0], color[1], color[2]))
            # point
            if len(obj) == 1:
                # Changing pens to make point bigger, instead of only one pixel
                painter.setPen(QPen(Qt.black, 3))
                painter.drawPoint(math.floor(obj[0].x), math.floor(obj[0].y))
                painter.setPen(Qt.black)
            # Lines and WireFrames
            for i in range(len(obj)-1):
                painter.drawLine(math.floor(obj[i].x),
                                 math.floor(obj[i].y),
                                 math.floor(obj[i+1].x),
                                 math.floor(obj[i+1].y))

        painter.setPen(Qt.black)
        self.__paint_limits(painter)

    def __paint_limits(self, painter):
        x, y = self.__offset.x, self.__offset.y
        painter.drawLine(x, y, self.__max_x - x, y)
        painter.drawLine(self.__max_x - x, y, self.__max_x - x, self.__max_y - y)
        painter.drawLine(self.__max_x - x, self.__max_y - y, x, self.__max_y - y)
        painter.drawLine(x, self.__max_y - y, x, y)
