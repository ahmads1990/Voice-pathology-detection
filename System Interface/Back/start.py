import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import threading
from WindowManager import WindowManager, PagesNumbers
from ModelHandler import ModelHandler
from Database.DatabaseHandler import DatabaseHandler

from PagesFolder.mainWindow import mainWindow
from PagesFolder.registerWindow import registerWindow
from PagesFolder.startSessionWindow import SessionWindow
from PagesFolder.recordsPatientWindow import recordsPatientsWindow
from PagesFolder.recordsSessionWindow import recordsSessionWindow
from PagesFolder.resultWindow import resultWindow
from PagesFolder.recordsPathologyWindow import recordsPathologyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    databaseHandler = DatabaseHandler()
    
    modelHandler = ModelHandler()
    modelHandler.loadModel()
    #modelHandler.modelPredict(0)
    
    windowManager = WindowManager()
    windowManager.AddWindow(mainWindow(windowManager), PagesNumbers.main)
    windowManager.AddWindow(registerWindow(windowManager,databaseHandler), PagesNumbers.register)
    windowManager.AddWindow(SessionWindow(windowManager,databaseHandler), PagesNumbers.session)
    windowManager.AddWindow(recordsPatientsWindow(windowManager,databaseHandler), PagesNumbers.recordsPatient)
    windowManager.AddWindow(recordsSessionWindow(windowManager,databaseHandler), PagesNumbers.recordsSession)
    windowManager.AddWindow(recordsPathologyWindow(windowManager,databaseHandler), PagesNumbers.recordsPathology)
    windowManager.AddWindow(resultWindow(windowManager,databaseHandler, modelHandler), PagesNumbers.results)
    windowManager.ShowWidget()
    
    sys.exit(app.exec_())