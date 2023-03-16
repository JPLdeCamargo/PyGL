from window import Window
from game_objects.coords2D import Coords2d
from game_objects.ABCObject import ABCObject
from game_objects.line import Line
from game_objects.wireframe import WireFrame

import sys
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

    def world_to_screen_coords(self) -> list[ABCObject]:
        viewport_objs = []
        world_objs_coords = self.__window.display_file
        for obj in world_objs_coords:

            # Transforming window coords into viewport coords
            viewport_coords = []
            for coord in obj.coords:
                transformed = self.__transform_to_viewport(coord)
                viewport_coords.append(transformed)

            if obj.is_closed:
                transformed = self.__transform_to_viewport(obj.coords[0])
                viewport_coords.append(transformed)


            viewport_objs.append(viewport_coords)
        return viewport_objs
            

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
        painter.setPen(Qt.red)

        objs = self.world_to_screen_coords()
        for obj in objs:
            for i in range(len(obj)-1):
                painter.drawLine(math.floor(obj[i].x),
                                 math.floor(obj[i].y),
                                 math.floor(obj[i+1].x),
                                 math.floor(obj[i+1].y))

            painter.drawLine(math.floor(obj[0].x),
                             math.floor(obj[0].y),
                             math.floor(obj[-1].x),
                             math.floor(obj[-1].y))

    def keyPressEvent(self, event):
        # Move window
        if event.key() == Qt.Key_Right:
            self.__window.move_x(100)
            self.update()
        elif event.key() == Qt.Key_Left:
            self.__window.move_x(-100)
            self.update()
        elif event.key() == Qt.Key_Up:
            self.__window.move_y(100)
            self.update()
        elif event.key() == Qt.Key_Down:
            self.__window.move_y(-100)
            self.update()
        
        # Zoom window
        elif event.key() == Qt.Key_W:
            self.__window.zoom(-100)
            self.update()
        elif event.key() == Qt.Key_S:
            self.__window.zoom(100)
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window(7000, 7000)
    ex = Viewport(1000, 1000, window)
    ex.resize(1000, 1000)
    ex.show()
    sys.exit(app.exec_())
