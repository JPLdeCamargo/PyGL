from .window import Window
from .viewport import Viewport
from .transform_options import TransformOptions


from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

class TransformController(QWidget):
    def __init__(self, window : Window, viewport : Viewport):
        super().__init__()
        self.__window = window
        self.__transform_options = TransformOptions(viewport)

        self.__list = QListWidget()
        self.__obj_map = {}
        for i in range(len(self.__window.display_file)):
            name = self.__window.display_file[i].name
            self.__list.insertItem(i, name)
            self.__obj_map[name] = self.__window.display_file[i]

        self.__list.clicked.connect(self.clicked_list)

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__list)
        self.__layout.addWidget(self.__transform_options)
        self.setLayout(self.__layout)

    def clicked_list(self):
        name = self.__list.currentItem().text()
        obj = self.__obj_map[name]
        self.__transform_options.update(name, obj)
