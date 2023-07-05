from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QLabel, QTextEdit, QPushButton,QTableWidgetItem
from PagesFolder.BaseWindow import BaseWindow
from Database.dtos import Patient
class registerWindow(QDockWidget):
    def __init__(self, windowManager, databaseHandler):
        super(registerWindow, self).__init__()
        self.windowManager = windowManager
        self.databaseHandler = databaseHandler
        
        # load the ui file
        uic.loadUi("../Front/register.ui", self)

        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/Register.png);")
        
        self.clearSession()
        # Assign functions
        self.btn_Cancel.clicked.connect(self.cancelSession)
        self.btn_Clear.clicked.connect(self.clearSession)
        self.btn_StartRecord.clicked.connect(self.startRecordSession)

    # change window go back to the main window
    def cancelSession(self):
        # go back
        self.windowManager.GoToMain()
        print("-- go back to main")
        
    # clear all the input fields
    def clearSession(self):
        self.txtEdit_Name.clear()
        self.txtEdit_Email.clear()
        self.txtEdit_Phone.clear()
        self.txtEdit_Age.clear()
        self.txtEdit_ID.clear()
        self.radbtn_male.setChecked(False)
        self.radbtn_female.setChecked(False)
        self.msg_Error.clear()

    def startRecordSession(self):  
        # check all fields     
        patientID = 0   
        name = self.txtEdit_Name.toPlainText()
        email = self.txtEdit_Email.toPlainText()
        phone = self.txtEdit_Phone.toPlainText()
        age = 0
        
        # try get age
        try: 
            age = int(self.txtEdit_Age.toPlainText())
        except:
            self.msg_Error.setText("Enter Age Correctly")
            
        if(age < 10 & age >90):
            self.msg_Error.setText("Enter Age Between (10~90)")
            return
        
        # try get id
        try: 
            patientID = int(self.txtEdit_ID.toPlainText())
        except:
            self.msg_Error.setText("Enter ID Correctly A Number")
        
        # get gender
        if (self.radbtn_male.isChecked() and self.radbtn_female.isChecked()) or \
            (not self.radbtn_male.isChecked() and not self.radbtn_female.isChecked()):
            self.msg_Error.setText("Must check one gender")
            return
        
        gender = ""
        gender = "m" if self.radbtn_male.isChecked() else "f"
        
        # if no fields are checked
        if name=="" or email==""or phone==""or phone==""or age=="" or gender == "":
            #print("Enter missing data Correctly")
            self.msg_Error.setText("Enter missing data !!")
            return
        
        # database
        newPatient = Patient(patientID,name,email,phone,age, gender)
        newPatient.print_attributes()
        try:
            self.databaseHandler.insert_patient(newPatient)
        except Exception as e:
            # Handle the exception and print the error message
            print("An error occurred:", str(e))
            print(self.databaseHandler)
            # update instead
            print("ID repeated")
            self.msg_Error.setText("ID repeated")
            return
        
        # all good then start recording
        self.msg_Error.clear()
        self.windowManager.GoToStartSession(patientID)
        print(patientID)
        print("Start recording")
