from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QLabel, QTextEdit, QPushButton,QTableWidgetItem

class recordsPatientsWindow(QDockWidget):
    def __init__(self, widgetManager, databaseHandler):
        super(recordsPatientsWindow, self).__init__()
        self.widgetManager = widgetManager
        self.databaseHandler = databaseHandler
        
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
        self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)
        self.btn_records_pathology.clicked.connect(self.switchWindowToRecordsPathology)

    def load_data(self):
        data = self.databaseHandler.all_data_patients()
        #print(data)
        row = 0
        self.tableWidget.setRowCount(len(data))
        for patient in data:
            id = f'{patient[0]}'
            age = f'{patient[2]}'
            self.tableWidget.setItem(row , 0 , QTableWidgetItem(id))
            self.tableWidget.setItem(row , 1 , QTableWidgetItem(patient[1]))
            self.tableWidget.setItem(row , 2 , QTableWidgetItem(age))
            self.tableWidget.setItem(row , 3 , QTableWidgetItem(patient[3]))
            self.tableWidget.setItem(row , 4 , QTableWidgetItem(patient[4]))
            self.tableWidget.setItem(row , 5 , QTableWidgetItem(patient[5]))
            row=row+1
        
    # change window
    def switchWindowToMain(self):
        self.widgetManager.GoToMain()
    
    def switchWindowToRecordsSession(self):
        self.widgetManager.GoToRecordsSession()
        
    def switchWindowToRecordsPathology(self):
        self.widgetManager.GoToRecordsPathology()
    