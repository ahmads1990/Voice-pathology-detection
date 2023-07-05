from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QLabel, QTextEdit, QPushButton,QTableWidgetItem
from PagesFolder.BaseWindow import BaseWindow
class mainWindow(QDockWidget):
    def __init__(self, windowManager):
        super(mainWindow, self).__init__()
        self.windowManager = windowManager
        #temp
        self.audioPath = "/Back/Audio/105-iau.wav"
        # load the ui file
        uic.loadUi("../Front/main.ui", self)

        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/Main.png);")
        
        # Assign functions
        self.StartSession.clicked.connect(self.switchWindowToRegister)
        # Side
        self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)
        self.btn_records_patient.clicked.connect(self.switchWindowToRecordsPatient)
        self.btn_records_pathology.clicked.connect(self.switchWindowToRecordsPathology)

    # change window
    def switchWindowToRegister(self):
        self.windowManager.GoToRegister()
        #self.windowManager.GoToResults()
        
    def switchWindowToRecordsSession(self):
        self.windowManager.GoToRecordsSession()
        
    def switchWindowToRecordsPatient(self):
        self.windowManager.GoToRecordsPatients()
    
    def switchWindowToRecordsPathology(self):
        self.windowManager.GoToRecordsPathology()
    