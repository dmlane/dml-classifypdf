""" View class for the dialog """

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow


class Pdfviewer(QMainWindow):
    """View class for the dialog"""

    def __init__(self):
        super().__init__()
        # self.menu = self.menuBar()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # | Qt.WindowType.SubWindow)
        # self.menu.setNativeMenuBar(False)
        # self.menu.setVisible(False)
        # self.menu.setHidden(True)
        # self.menuBar().setHidden(True)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        # self.setWindowFlag(Qt.WindowType.WindowSystemMenuHint, False)
        # set the title
        self.setWindowTitle("no title")
        self.setGeometry(100, 100, 400, 300)

        # creating a label widget
        # by default label will display at top left corner
        self.label_1 = QLabel("no title bar", self)

        # moving position
        self.label_1.move(100, 100)

        # setting up border and background color
        self.label_1.setStyleSheet("background-color: lightgreen;border: 3px solid green")
