from enum import Enum
from PyQt5 import QtWidgets


class PagesNumbers(Enum):
    main=0
    register=1
    session=2
    recordsSession=3
    recordsPatient=4
    recordsPathology=5
    results=6
    
class WindowManager():
    def __init__(self):
        print("WindowManager")
        self.widgetManager = QtWidgets.QStackedWidget()
        
        self.dict = {}
        self.count = 0
        
    def ShowWidget(self):
        self.widgetManager.show()
        
    def AddWindow(self,newWindow, pageEnum):
        #print(f"Debug: Widgets Count Before is {self.widgetManager.count()}")
        self.widgetManager.addWidget(newWindow)
        self.dict.update({pageEnum: self.count})
        self.count += 1
        
        #print(f"Debug: Widgets Count After is {self.widgetManager.count()}")
        #print(f"Debug: Added new window {pageEnum}")
    
    def GoToMain(self):
        index = self.dict[PagesNumbers.main]
        self.widgetManager.setCurrentIndex(index)
        
    def GoToRegister(self):
        index = self.dict[PagesNumbers.register]
        self.widgetManager.widget(index).clearSession()
        self.widgetManager.setCurrentIndex(index)
    
    def GoToStartSession(self, patientID):
        index = self.dict[PagesNumbers.session]
        window = self.widgetManager.widget(index)
        window.setPatientID(patientID)
        self.widgetManager.setCurrentIndex(index)
    
    def GoToResults(self, sessionDto): 
        index = self.dict[PagesNumbers.results]       
        self.widgetManager.widget(index).setSessionDto(sessionDto)
        self.widgetManager.widget(index).sendToModelPredict()
        self.widgetManager.setCurrentIndex(index)

    def GoToRecordsSession(self):
        index = self.dict[PagesNumbers.recordsSession]
        self.widgetManager.widget(index).load_data()
        self.widgetManager.setCurrentIndex(index)
        
    def GoToRecordsPatients(self):
        index = self.dict[PagesNumbers.recordsPatient]
        self.widgetManager.widget(index).load_data()
        self.widgetManager.setCurrentIndex(index)
    
    def GoToRecordsPathology(self):
        index = self.dict[PagesNumbers.recordsPathology]
        #self.widgetManager.widget(index).load_data()
        self.widgetManager.setCurrentIndex(index)