from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QDockWidget,QTableWidgetItem, QScrollArea, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
#from Database.database import all_data_sessions

class recordsPathologyWindow(QDockWidget):
    def __init__(self, widgetManager, databaseHandler):
        super(recordsPathologyWindow, self).__init__()
        self.windowManager = widgetManager   
        self.databaseHandler = databaseHandler
        
        self.document = databaseHandler.fetch_pathologies()
        
        # load the ui file 
        uic.loadUi("../Front/recordsPathology.ui", self)
        self.pathologyLabel.setReadOnly(True)
        self.pathologyLabel.setFont(QFont('Arial', 15))
        
        # set background image
        self.background.setStyleSheet(f"background-image: url(../Front/Images/ShowDisorders.png);")

        self.load_ScrollBar()
        # Side
        self.btn_main.clicked.connect(self.switchWindowToMain)
        self.btn_records_session.clicked.connect(self.switchWindowToRecordsSession)
        self.btn_records_patient.clicked.connect(self.switchWindowToRecordsPatient)
        
    def returnButton(self, name):
        pushButton = QPushButton()
        pushButton.setObjectName(name)
        pushButton.setGeometry (QtCore.QRect(20, 10, 250, 50))
        pushButton.setStyleSheet("""background-image: url();
                                background-color: rgb(255, 252, 255);
                                border-radius: 10px;
                                text-align:center;
                                color:rgb(69, 77, 179);
                                font-size: 12px;
                                font-weight: bold;
                                Height:40px""")
        pushButton.setText (name)
        return pushButton

    def createButtonClickedCallback(self, parameter):
            def button_clicked():
                self.pathologyLabel.setText(str(parameter))
            return button_clicked
    
    def load_ScrollBar(self):
        self.scroll_area = self.scrollArea
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Create and add multiple buttons to the layout
        buttons = []
        for i in range(1, len(self.document) + 1):
            button = self.returnButton(f"{self.document[i][0]}")
            buttons.append(button)
            self.layout.addWidget(button)
            #buttons[i].clicked.connect(lambda: self.setLabel(i))
            button.clicked.connect(self.createButtonClickedCallback(self.document[i][1]))

        # Set the widget as the content of the scroll area
        self.scroll_area.setWidget(self.widget)
        # Set scroll area properties (optional)
        self.scroll_area.setWidgetResizable(True)  # Allows the widget to resize with the scroll area
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrollbar
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    
    # change window
    def switchWindowToMain(self):
        self.windowManager.GoToMain()
    
    def switchWindowToRecordsSession(self):
        self.windowManager.GoToRecordsSession()
        
    def switchWindowToRecordsPatient(self):
        self.windowManager.GoToRecordsPatients()