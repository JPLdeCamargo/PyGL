from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets

from .window import Window
from .viewport import Viewport
from .enums.obj_types import ObjTypes
from .game_objects.wireframe import WireFrame
from .game_objects.line import Line
from .game_objects.point import Point
from .transform_controller import TransformController


class CreateObjWindow(QWidget):
    def __init__(self, window : Window, viewport : Viewport, transform_controller = TransformController):
        super().__init__()
        self.__window = window
        self.__viewport = viewport
        self.__transform_controller = transform_controller
        self.__color = (0, 0, 0)

        self.__layout = QGridLayout()
        self.__welcome = QLabel("Select which object type you would like to create")

        line_radio = QRadioButton("Line")
        line_radio.type = ObjTypes.LINE
        line_radio.clicked.connect(self.clicked_radio)

        point_radio = QRadioButton("Point")
        point_radio.type = ObjTypes.POINT
        point_radio.clicked.connect(self.clicked_radio)
        point_radio.setChecked(True)
        self.__type = ObjTypes.POINT

        wire_radio = QRadioButton("Wireframe")
        wire_radio.type = ObjTypes.WIREFRAME
        wire_radio.clicked.connect(self.clicked_radio)

        self.__closed_wire_checkbox = QCheckBox("Closed", self)

        name_label = QLabel("Name")
        self.__name_input = QLineEdit(self)

        coords_label = QLabel("Coordinates")
        self.__helper = QLabel("Format = (x1, y1), (x2, y2), ...")
        self.__coords_input = QLineEdit(self)

        self.__create_button = QPushButton("Create")
        self.__create_button.clicked.connect(self.create)
        
        self.__choose_color = QPushButton("Color")
        self.__choose_color.clicked.connect(self.choose_color)

        self.__layout.addWidget(self.__welcome, 0, 0)
        self.__layout.addWidget(line_radio, 1, 0)
        self.__layout.addWidget(point_radio, 1, 1)
        self.__layout.addWidget(wire_radio, 1, 2)
        self.__layout.addWidget(self.__closed_wire_checkbox, 2, 0)
        self.__closed_wire_checkbox.close()
        self.__layout.addWidget(name_label, 3, 0)
        self.__layout.addWidget(self.__name_input, 3, 1, 1, 2)
        self.__layout.addWidget(coords_label, 4, 0)
        self.__layout.addWidget(self.__coords_input, 4, 1, 1, 2)
        self.__layout.addWidget(self.__helper, 5, 0, 1, 3)
        self.__layout.addWidget(self.__create_button, 6, 2)
        self.__layout.addWidget(self.__choose_color, 7, 2)
    

        self.setLayout(self.__layout)

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.__color = color.getRgb()

    def create(self):
        name = self.__name_input.text()
        # checking name availability
        if name == "" or self.__window.get_obj(name) != False or len(name) > 10:
            self.__helper.setText("Name not available")
            return

        coords = self.test_coords(self.__coords_input.text(), self.__type) 
        # checking coordinates format
        if coords != False:
            obj = None
            if self.__type == ObjTypes.WIREFRAME:
                if len(coords) < 3:
                    self.__helper.setText("Coordinates input not accepted")
                    return
                is_closed = self.__closed_wire_checkbox.isChecked()
                obj = WireFrame(name, is_closed, coords, self.__color)

            elif self.__type == ObjTypes.LINE:
                if len(coords) != 2:
                    self.__helper.setText("Coordinates input not accepted")
                    return
                obj = Line(name, coords[0], coords[1], self.__color)
                
            elif self.__type == ObjTypes.POINT:
                if len(coords) != 1:
                    self.__helper.setText("Coordinates input not accepted")
                    return
                obj = Point(name, coords[0], self.__color)

            self.__window.add_to_display_file(obj)
            self.__window.update_normalized()
            self.__viewport.update()
            self.__transform_controller.update_list()
            self.close()

        else:
            self.__helper.setText("Coordinates input not accepted")
            return
            

    def test_coords(self, coords : str, type : ObjTypes) -> bool:
        coords = coords.replace(" ", "")
        coords = list(coords)

        # Checking if parenthesis are correct
        inside = False
        for i in range(len(coords)):
            if coords[i] == "(":
                if inside == True:
                    return False
                coords[i] = ""
                inside = True
            if coords[i] == ")":
                if inside == False:
                    return False
                coords[i] = ""
                inside = False
            if coords[i] == "," and inside == False:
                coords[i] = "|"
        coords = "".join(coords)

        points = coords.split("|")
        to_return = []
        for point in points:
            try:
                xs, ys = point.split(",")
                to_return.append((float(xs), float(ys)))
            except:
                return False

        return to_return
            
    def clicked_radio(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.__type = radioButton.type
        if radioButton.type == ObjTypes.WIREFRAME:
            self.__closed_wire_checkbox.show()
        else:
            self.__closed_wire_checkbox.close()
