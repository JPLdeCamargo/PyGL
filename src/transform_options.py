from .viewport import Viewport
from .game_objects.ABCObject import ABCObject


from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

class TransformOptions(QWidget):
    def __init__(self, viewport : Viewport):
        super().__init__()
        self.__reminder = QLabel("Currently editing: None")
        self.__current = None
        self.__viewport = viewport

        self.__help = QLabel(f"Please fill the inputs correctly")

        tabs = QTabWidget()
        layout = QGridLayout()

        # Making translate tab
        vx_text = QLabel("x")
        self.__translate_x = QLineEdit(self)
        vy_text = QLabel("y")
        self.__translate_y = QLineEdit(self)
        submit = QPushButton("apply")
        submit.clicked.connect(self.apply_translate)
        translate_widget = QWidget()
        translate_layout = QGridLayout()
        translate_layout.addWidget(vx_text, 0, 0)
        translate_layout.addWidget(self.__translate_x, 0, 1)
        translate_layout.addWidget(vy_text, 1, 0)
        translate_layout.addWidget(self.__translate_y, 1, 1)
        translate_layout.addWidget(submit, 2, 0, 1, 2)
        translate_widget.setLayout(translate_layout)
        tabs.addTab(translate_widget, "Translate")

        # Making scale tab
        vx_text_scale = QLabel("x")
        self.__scale_x = QLineEdit(self)
        vy_text_scale = QLabel("y")
        self.__scale_y = QLineEdit(self)
        submit_scale = QPushButton("apply")
        submit_scale.clicked.connect(self.apply_scale)
        scale_widget = QWidget()
        scale_layout = QGridLayout()
        scale_layout.addWidget(vx_text_scale, 0, 0)
        scale_layout.addWidget(self.__scale_x, 0, 1)
        scale_layout.addWidget(vy_text_scale, 1, 0)
        scale_layout.addWidget(self.__scale_y, 1, 1)
        scale_layout.addWidget(submit_scale, 2, 0, 1, 2)
        scale_widget.setLayout(scale_layout)
        tabs.addTab(scale_widget, "Scale")

        # Making Rotation tab
        angle_text_rotation = QLabel("Angle (degrees)")
        self.__angle = QLineEdit(self)
        submit_rotation = QPushButton("apply")
        submit_rotation.clicked.connect(self.apply_rotation)
        rotation_widget = QWidget()
        rotation_layout = QGridLayout()
        rotation_layout.addWidget(angle_text_rotation, 0, 0)
        rotation_layout.addWidget(self.__angle, 0, 1)
        rotation_layout.addWidget(submit_rotation, 1, 0, 1, 2)
        rotation_widget.setLayout(rotation_layout)
        tabs.addTab(rotation_widget, "Rotation")
        
        layout.addWidget(self.__reminder)
        layout.addWidget(self.__help)
        layout.addWidget(tabs)
        self.setLayout(layout)

    def apply_translate(self):
        try:
            vx = float(self.__translate_x.text())
            vy = float(self.__translate_y.text())
            self.__current.translate(vx, vy)
            self.__viewport.update()
            self.__help.setText(f"Translating {self.__current.name}")

        except:
            self.__help.setText("Input type not suported")

    def apply_scale(self):
        try:
            vx = float(self.__scale_x.text())
            vy = float(self.__scale_y.text())
            self.__current.scale(vx, vy)
            self.__viewport.update()
            self.__help.setText(f"Scaling {self.__current.name}")

        except:
            self.__help.setText("Input type not suported")

    def apply_rotation(self):
        try:
            angle = float(self.__angle.text())
            self.__current.rotate(angle)
            self.__viewport.update()
            self.__help.setText(f"Rotating {self.__current.name}")

        except:
            self.__help.setText("Input type not suported")

    def update(self, name : str, obj : ABCObject):
        self.__reminder.setText(f"Currently editing: {name}")
        self.__current = obj
            