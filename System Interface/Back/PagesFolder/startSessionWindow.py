from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QLabel, QTextEdit, QPushButton,QTableWidgetItem
from AudioRecorder import Recorder
import threading

from Database.dtos import Session
class SessionWindow(QDockWidget):
    def __init__(self, widgetManager, databaseHandler):
        super(SessionWindow, self).__init__()
        self.widgetManager = widgetManager
        self.databaseHandler = databaseHandler
        
        self.AudioRecorder = Recorder()

        # data
        self.patientID = 0
        self.audioPath = 'Audio/'
        # record 1  
        self.part1_IsRecorded = False
        self.part1_Type = "iau"  
        # record 2  
        self.part2_IsRecorded = False
        self.part2_Type = "phrase"    
        
        # load the ui file
        uic.loadUi("../Front/Session.ui", self)

        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/StartSession.png);")

        # Assign functions
        self.RecordPart1_Btn.clicked.connect(self.recordPart1)
        self.RecordPart2_Btn.clicked.connect(self.recordPart2)
        self.EndSession_btn.clicked.connect(self.endRecordSession)

    def setPatientID (self, patientID = 0):
        self.patientID = patientID
        self.sessionID = self.databaseHandler.select_last_session_id() + 1
        print("idddddddddddd         " + str(self.sessionID))
        self.part1_Type_Path = str(self.sessionID)+"-"+self.part1_Type
        self.part2_Type_Path = str(self.sessionID)+"-"+self.part2_Type
        
    # Start recording part 1
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
        self.part1_IsRecorded = not self.part1_IsRecorded

    # Start recording part 2
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
        self.part2_IsRecorded = not self.part2_IsRecorded

    def endRecordSession(self):
        # finish recording
        newSession = Session(self.patientID, self.audioPath, -1,"",self.part1_IsRecorded , self.part2_IsRecorded)
        
        sessionId = self.databaseHandler.insert_session(newSession)      
        newSession.id = sessionId

        newSession.print_attributes()
        self.widgetManager.GoToResults(newSession)