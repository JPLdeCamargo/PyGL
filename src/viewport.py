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

            # Transforming window coords into viewport coords
            viewport_coords = []
            colors.append(obj.color)
            for coord in obj.coords:
                transformed = self.__transform_to_viewport(coord)
                viewport_coords.append(transformed)

            if obj.is_closed:
                transformed = self.__transform_to_viewport(obj.coords[0])
                viewport_coords.append(transformed)


            viewport_objs.append(viewport_coords)
        return (viewport_objs, colors)
            

    def __transform_to_viewport(self, point:Coords2d) -> Coords2d:
        boundry_coord = Coords2d(self.__max_x - self.__min_x, self.__max_y - self.__min_y)
        unit = self.__transform_into_unitary(point)
        transformed = unit * boundry_coord
        transformed = Coords2d(math.floor(transformed.x), math.floor(transformed.y))
        return transformed

                 
    # Unitary values to where the point will be
    # relatively to its position on the window coordinates
    def __transform_into_unitary(self, point:Coords2d) -> Coords2d:
        unit_x = (point.x - self.__window.min_x)/(self.__window.max_x - self.__window.min_x)
        unit_y = 1 - ((point.y - self.__window.min_y)/(self.__window.max_y - self.__window.min_y))
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
