from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication,QTableWidgetItem


class BaseWindow(QDockWidget):
    def __init__(self, windowManager):
        super().__init__()
        
        self.windowManager = windowManager
        # set the title
        self.setWindowTitle("GradProject")
        # load the ui file
        uic.loadUi("../Front/main.ui", self)