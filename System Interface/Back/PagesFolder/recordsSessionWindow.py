from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QLabel, QTextEdit, QPushButton,QTableWidgetItem
#from Database.database import all_data_sessions

class recordsSessionWindow(QDockWidget):
    def __init__(self, widgetManager, databaseHandler):
        super(recordsSessionWindow, self).__init__()
        self.widgetManager = widgetManager   
        self.databaseHandler = databaseHandler
        
        # load the ui file 
        uic.loadUi("../Front/recordsSession.ui", self)
        
        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/ShowRecordsSession.png);")
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.setColumnWidth(3, 90)
        self.tableWidget.setColumnWidth(2, 300)

        self.load_data()
        
        # Side
        self.btn_main.clicked.connect(self.switchWindowToMain)
        self.btn_records_patient.clicked.connect(self.switchWindowToRecordsPatient)

    
    def load_data(self):
        data = self.databaseHandler.all_data_sessions()
        #print(data)
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
        self.widgetManager.GoToMain()
    
    def switchWindowToRecordsPatient(self):
        self.widgetManager.GoToRecordsPatients()