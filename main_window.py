import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from viewport import Viewport
from window import Window

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.__window = Window(7000, 7000)
        self.__viewport = Viewport(500, 500, self.__window)
        self.__viewport.resize(500, 500)
        self.setWindowTitle("Viewport Transform")

        layout = QGridLayout()
        layout.addWidget(self.__viewport, 0,0)

        right = QPushButton("right")
        right.clicked.connect(self.clicked_right)
        layout.addWidget(right, 2,1,alignment=Qt.AlignmentFlag.AlignHCenter)

        left = QPushButton("left")
        left.clicked.connect(self.clicked_left)
        layout.addWidget(right, 2,0)

        up = QPushButton("up")
        up.clicked.connect(self.clicked_up)
        layout.addWidget(up, 1,0,alignment=Qt.AlignmentFlag.AlignHCenter)

        down = QPushButton("down")
        down.clicked.connect(self.clicked_down)
        layout.addWidget(down, 3,0)

        self.setLayout(layout)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = MainWindow()
    test.show()
    test.resize(500, 500)
    sys.exit(app.exec_())