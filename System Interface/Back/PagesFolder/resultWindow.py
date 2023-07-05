from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QLabel, QTextEdit, QPushButton,QTableWidgetItem
from ModelHandler import ModelHandler
from Model.test_binary_model import load_model, test_model
import threading
import keras

class resultWindow(QDockWidget):
    def __init__(self, windowManager,databaseHandler, modelHandler):
        super(resultWindow, self).__init__()
        self.windowManager = windowManager
        self.databaseHandler = databaseHandler
        self.modelHandler = modelHandler

        self.sessionDto = None
        self.audioPath = "Audio/105-iau.wav"

        # load the ui file
        uic.loadUi("../Front/result.ui", self)
        
        # set background image
        self.background.setStyleSheet(
            f"background-image: url(../Front/Images/Results.png);"
        )
        
        self.clearAllFields()
        # Assign functions
        self.GoBack.clicked.connect(self.switchWindowToMain)

    def setSessionDto(self, sessionDto):
        self.sessionDto = sessionDto
        self.patientDto = self.databaseHandler.select_patient_by_id(self.sessionDto.patient_id)

    def sendToModelPredict(self):
        print("-------------------")
        print(self.modelHandler.model)

        self.result = self.modelHandler.modelPredict(self.sessionDto)
        self.result = self.result.lower()
        
        self.pathologyDto = self.databaseHandler.get_pathology_by_name(self.result)
        print(self.pathologyDto)
        print(self.result)
        self.pathologyDto.print_attributes()
        
        if(self.result == "healthy"):
            self.background.setStyleSheet(
            f"background-image: url(../Front/Images/ResultsHealthy.png);")
        else:
            self.background.setStyleSheet(
            f"background-image: url(../Front/Images/ResultsPathology.png);")

        self.setAllFields()
        self.databaseHandler.update_session_pathology_id(self.sessionDto.id, self.pathologyDto.id)

    # clear all the fields
    def clearAllFields(self):
        self.txtEdit_ID.clear()
        self.txtEdit_Name.clear()
        self.txtEdit_Email.clear()
        self.txtEdit_Phone.clear()
        self.txtEdit_Age.clear() 
        self.txtEdit_Gender.clear()
        self.txtEdit_Diagnosis.clear()

    # set all the fields
    def setAllFields(self):
        self.txtEdit_ID.setText(str(self.patientDto.id))
        self.txtEdit_Name.setText(self.patientDto.name)
        self.txtEdit_Email.setText(self.patientDto.email)
        self.txtEdit_Phone.setText(str(self.patientDto.phone))
        self.txtEdit_Age.setText(str(self.patientDto.age)) 
        self.txtEdit_Gender.setText(self.patientDto.gender)
        self.txtEdit_Diagnosis.setText(self.pathologyDto.name)

    # change window
    def switchWindowToMain(self):
        self.windowManager.GoToMain()