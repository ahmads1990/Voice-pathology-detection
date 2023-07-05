from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication,QTableWidgetItem
from AudioRecorder import Recorder
import threading
from Database.database import all_data_patients, all_data_sessions, insert_patient, insert_session

class BaseWindow(QDockWidget):
    def __init__(self):
        super().__init__()
        # load the ui file
        uic.loadUi("../Front/main.ui", self)
        
class mainWindow(QDockWidget):
    def __init__(self, widgetManager, changeWindow):
        super(mainWindow, self).__init__()
        self.widgetManager = widgetManager
        self.changeWindow = changeWindow
        
        #temp
        self.audioPath = "/Back/Audio/105-iau.wav"
        # load the ui file
        uic.loadUi("../Front/main.ui", self)

        # set background image
        self.background.setStyleSheet(
            f"background-image: url(../Front/Images/Main.png);"
        )

        # Assign functions
        self.StartSession.clicked.connect(self.switchWindowToRegister)
        
        # Side
        #self.btn_main.clicked.connect(self.switchWindowToRegister)
        self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)
        self.btn_records_patient.clicked.connect(self.switchWindowToRecordsPatient)

    # go to diangosed
    def switchToResultsPage(self):
        newWindow = recordsSessionWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)
        global model
        model.test_model(self.audioPath)
        
    # change window
    def switchWindowToRegister(self):
        newWindow = registerWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)
        
    def switchWindowToRecordsSession(self):
        newWindow = recordsSessionWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)
        
    def switchWindowToRecordsPatient(self):
        newWindow = recordsPatientsWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)

class registerWindow(QDockWidget):
    def __init__(self, widgetManager, changeWindow):
        super(registerWindow, self).__init__()
        self.widgetManager = widgetManager
        self.changeWindow = changeWindow

        #todo gen error message
        #self.msg_Error.setText("")
        # load the ui file
        uic.loadUi("../Front/register.ui", self)

        # set background image
        self.background.setStyleSheet(
            f"background-image: url(../Front/Images/Register.png);"
        )

        # Assign functions
        self.btn_Cancel.clicked.connect(self.cancelSession)
        self.btn_Clear.clicked.connect(self.clearSesssion)
        self.btn_StartRecord.clicked.connect(self.startRecordSession)

    # change window go back to the main window
    def cancelSession(self):
        # go back
        self.widgetManager.removeWidget(self)
        print("go back")
        
    # clear all the input fields
    def clearSesssion(self):
        self.txtEdit_Name.clear()
        self.txtEdit_Email.clear()
        self.txtEdit_Phone.clear()
        self.txtEdit_Age.clear()

        self.radbtn_male.setChecked(False)
        self.radbtn_female.setChecked(False)
        print("clear")

    def startRecordSession(self):  
        # check all fields
        self.patientID = self.txtEdit_ID.toPlainText()
        name = self.txtEdit_Name.toPlainText()
        email = self.txtEdit_Email.toPlainText()
        phone = self.txtEdit_Phone.toPlainText()
        age = self.txtEdit_Age.toPlainText()
        
        # Todo: add more validation
        if self.radbtn_male.isChecked() and self.radbtn_female.isChecked():
            return

        gender = ""
        gender = "m" if self.radbtn_male.isChecked() else "f"
        
        if name=="" or email==""or phone==""or phone==""or age=="" or gender == "":
            print("Enter data")
            self.msg_Error.setText("Enter data")
            return
        # database
        insert_patient(self.patientID, name, age,gender, phone, email)
        
        # all good then start recording
        newWindow = SessionWindow(self.widgetManager, self.changeWindow, self.patientID)
        self.changeWindow(self.widgetManager, newWindow)
        
        print("Start recording")

class SessionWindow(QDockWidget):
    def __init__(self, widgetManager, changeWindow, patientID):
        super(SessionWindow, self).__init__()
        self.widgetManager = widgetManager
        self.changeWindow = changeWindow
        self.patientID = patientID
        
        self.AudioRecorder = Recorder()

        # data
        self.part1_IsRecorded = False
        self.part1_Type = "Letters"
        self.part1_Type_Path = self.part1_Type+"_"+str(self.patientID)
        
        self.part2_IsRecorded = False
        self.part2_Type = "Phrases"
        self.part2_Type_Path = self.part2_Type+"_"+str(self.patientID)
        
        # load the ui file
        uic.loadUi("../Front/Session.ui", self)

        # set background image
        self.background.setStyleSheet(
            f"background-image: url(../Front/Images/StartSession.png);"
        )

        # Assign functions
        self.RecordPart1_Btn.clicked.connect(self.recordPart1)
        self.RecordPart2_Btn.clicked.connect(self.recordPart2)

        self.EndSession_btn.clicked.connect(self.switchWindow)

    # Start recording
    def recordPart1(self):
        self.RecordPart1_Slider.setValue(int(0))
        if not self.AudioRecorder.is_recording:
            threading.Thread(
                target=self.AudioRecorder.start_recording,
                args=(
                    self.part1_Type_Path,
                    self.RecordPart1_Bar_Label,
                    self.RecordPart1_Slider,
                ),
            ).start()
        else:
            self.AudioRecorder.stop_recording()

    # Start recording
    def recordPart2(self):
        self.RecordPart2_Slider.setValue(int(0))
        if not self.AudioRecorder.is_recording:
            threading.Thread(
                target=self.AudioRecorder.start_recording,
                args=(
                    self.part2_Type_Path,
                    self.RecordPart2_Bar_Label,
                    self.RecordPart2_Slider,
                ),
            ).start()
        else:
            self.AudioRecorder.stop_recording()

    def switchWindow(self):
        #if self.part1_IsRecorded and self.part2_IsRecorded:
        
        part1_IsRecorded = ""
        part2_IsRecorded = ""
        if self.part1_IsRecorded:
            part1_IsRecorded="DONE"
        if self.part2_IsRecorded:
            part2_IsRecorded="DONE"
            
        # finish recording
        insert_session(self.patientID, "", "","", part1_IsRecorded, part2_IsRecorded)
        self.widgetManager.removeWidget(self)
        print(f"removed widget and count is {self.widgetManager.count()}")
        self.widgetManager.removeWidget(self.widgetManager.widget(int(self.widgetManager.count())-1))
        print(f"removed widget and count is {self.widgetManager.count()}")
        widget = self.widgetManager.widget(int(self.widgetManager.count())-1)
        widget.switchToResultsPage()
        
class recordsPatientsWindow(QDockWidget):
    def __init__(self, widgetManager, changeWindow):
        super(recordsPatientsWindow, self).__init__()
        self.widgetManager = widgetManager
        self.changeWindow = changeWindow      
        
        # load the ui file 
        uic.loadUi("../Front/recordsPatients.ui", self)
        
        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/ShowRecordsPatients.png);") 
        self.tableWidget.setColumnWidth(0,51)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2,100)
        self.tableWidget.setColumnWidth(3,140)
        self.tableWidget.setColumnWidth(4,240)

        self.load_data()
        
        # Side
        self.btn_main.clicked.connect(self.switchWindowToMain)
        #self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)
        self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)

    def load_data(self):
        data = all_data_patients()
        print(data)
        row = 0
        self.tableWidget.setRowCount(len(data))
        for patient in data:
            id = f'{patient[0]}'
            age = f'{patient[2]}'
            self.tableWidget.setItem(row , 0 , QTableWidgetItem(id))
            self.tableWidget.setItem(row , 1 , QTableWidgetItem(patient[1]))
            self.tableWidget.setItem(row , 2 , QTableWidgetItem(age))
            self.tableWidget.setItem(row , 3 , QTableWidgetItem(patient[2]))
            self.tableWidget.setItem(row , 4 , QTableWidgetItem(patient[3]))
            self.tableWidget.setItem(row , 5 , QTableWidgetItem(patient[4]))
            row=row+1

    # change window
    def switchWindowToMain(self):
        newWindow = mainWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)
    
    def switchWindowToRecordsSession(self):
        newWindow = recordsSessionWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)
        
class recordsSessionWindow(QDockWidget):
    def __init__(self, widgetManager, changeWindow):
        super(recordsSessionWindow, self).__init__()
        self.widgetManager = widgetManager
        self.changeWindow = changeWindow      
        
        # load the ui file 
        uic.loadUi("../Front/recordsSession.ui", self)
        
        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/ShowRecordsSession.png);")
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.setColumnWidth(3, 90)
        # self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 300)
        # self.tableWidget.setColumnWidth(3, 140)
        # self.tableWidget.setColumnWidth(4, 240)

        self.load_data()
        
        # Side
        self.btn_main.clicked.connect(self.switchWindowToMain)
        #self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)
        self.btn_records_patient.clicked.connect(self.switchWindowToRecordsPatient)

    def load_data(self):
        data = all_data_sessions()
        print(data)
        row = 0
        self.tableWidget.setRowCount(len(data))
        for session in data:
            id_patient = f'{session[0]}'
            id_session = f'{session[1]}'
            id_pathology = f'{session[3]}'

            self.tableWidget.setItem(row, 0, QTableWidgetItem(id_patient))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(id_session))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(session[2]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(id_pathology))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(session[4]))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(session[4]))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(session[4]))
            row = row + 1
        
    # change window
    def switchWindowToMain(self):
        newWindow = mainWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)
    
    def switchWindowToRecordsPatient(self):
        newWindow = recordsPatientsWindow(self.widgetManager, self.changeWindow)
        self.changeWindow(self.widgetManager, newWindow)