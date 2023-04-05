from src.gui.main_window import MainWindow

import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = MainWindow()
    test.show()
    test.resize(500, 500)
    sys.exit(app.exec_())