from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

import os

from ..cg_classes.viewport import Viewport
from ..cg_classes.window import Window
from .transform_controller import TransformController
from .create_obj_window import CreateObjWindow
from ..cg_classes.wavefront_manager import WavefrontManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__wavefront_manager = WavefrontManager(os.path.join(os.getcwd(), "obj_files"))

        self.__window = Window(7000, 7000, self.__wavefront_manager.load_all())
        self.__viewport = Viewport(500, 500, self.__window)
        self.__viewport.resize(500, 500)

        self.setWindowTitle("Viewport Transform")

        layout = QGridLayout()
        self.__viewport.setMinimumHeight(500)
        self.__viewport.setMinimumWidth(500)
        layout.addWidget(self.__viewport, 0,0,8,8)
        
        # Buttons
        buttons_widget = QWidget()
        buttons_layout = QGridLayout()
        label = QLabel("Window")
        buttons_layout.addWidget(label, 0,1)

        right = QPushButton("right")
        right.clicked.connect(self.clicked_right)
        buttons_layout.addWidget(right, 2,2)

        left = QPushButton("left")
        left.clicked.connect(self.clicked_left)
        buttons_layout.addWidget(left, 2,1)

        up = QPushButton("up")
        up.clicked.connect(self.clicked_up)
        buttons_layout.addWidget(up, 1,1,1,2)

        down = QPushButton("down")
        down.clicked.connect(self.clicked_down)
        buttons_layout.addWidget(down,4,1,1,2)

        plus = QPushButton("+")
        plus.clicked.connect(self.clicked_plus)
        buttons_layout.addWidget(plus,2,4)

        minus = QPushButton("-")
        minus.clicked.connect(self.clicked_minus)
        buttons_layout.addWidget(minus,2,0)

        rotate_label = QLabel("Rotate window")
        buttons_layout.addWidget(rotate_label, 5, 0)

        self.__rotate_input = QLineEdit(self)
        buttons_layout.addWidget(self.__rotate_input, 5, 1)

        rotate_submit = QPushButton("Rotate")
        rotate_submit.clicked.connect(self.rotate_window)
        buttons_layout.addWidget(rotate_submit, 5, 2)

        buttons_widget.setLayout(buttons_layout)

        layout.addWidget(buttons_widget, 9,4)
        
        # Transformations controller
        self.__transform_controller = TransformController(self.__window, self.__viewport)
        layout.addWidget(self.__transform_controller, 4, 9)

        # Create Object button
        self.__create_obj_window = None
        create = QPushButton("Create new object")
        create.clicked.connect(self.create_obj)
        layout.addWidget(create, 9, 0)

        self.setLayout(layout)

    def rotate_window(self):
        text = self.__rotate_input.text()
        try:
            self.__window.rotate(float(text), self.__window.up_vector)

            self.__viewport.update()
        except:
            return
        

    def clicked_right(self):
        self.__window.move_x(100)
        self.__viewport.update()

    def clicked_left(self):
        self.__window.move_x(-100)
        self.__viewport.update()

    def clicked_up(self):
        self.__window.move_y(100)
        self.__viewport.update()

    def clicked_down(self):
        self.__window.move_y(-100)
        self.__viewport.update()

    def clicked_plus(self):
        self.__window.zoom(100)
        self.__viewport.update()

    def clicked_minus(self):
        self.__window.zoom(-100)
        self.__viewport.update()

    def create_obj(self):
        if self.__create_obj_window is None:
            self.__create_obj_window = CreateObjWindow(self.__window, 
                                                       self.__viewport,
                                                       self.__transform_controller,
                                                       self.__wavefront_manager)
        self.__create_obj_window.show()

    def closeEvent(self, event):
            self.__wavefront_manager.backup_files(self.__window.display_file)

            event.accept() 
