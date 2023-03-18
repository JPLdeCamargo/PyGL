import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from viewport import Viewport
from window import Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__window = Window(7000, 15000)
        self.__viewport = Viewport(500, 500, self.__window)
        self.__viewport.resize(500, 500)
        self.setWindowTitle("Viewport Transform")

        layout = QGridLayout()
        self.__viewport.setMinimumHeight(500)
        self.__viewport.setMinimumWidth(500)
        layout.addWidget(self.__viewport, 0,0,8,9)
        
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

        buttons_widget.setLayout(buttons_layout)

        layout.addWidget(buttons_widget, 9,4)
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

    def clicked_plus(self):
        self.__window.zoom(-100)
        self.__viewport.update()

    def clicked_minus(self):
        self.__window.zoom(100)
        self.__viewport.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = MainWindow()
    test.show()
    test.resize(500, 500)
    sys.exit(app.exec_())