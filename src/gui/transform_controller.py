from ..cg_classes.window import Window
from ..cg_classes.viewport import Viewport
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
        for i in range(len(self.__window.display_file)):
            name = self.__window.display_file[i].name
            self.__list.insertItem(i, name)
        self.__list.clicked.connect(self.clicked_list)

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__list)
        self.__layout.addWidget(self.__transform_options)
        self.setLayout(self.__layout)

    def clicked_list(self):
        name = self.__list.currentItem().text()
        obj = self.__window.get_obj(name)
        self.__transform_options.update(name, obj)

    def update_list(self):
        obj = self.__window.display_file[-1]
        self.__list.insertItem(len(self.__window.display_file) - 1, obj.name)
