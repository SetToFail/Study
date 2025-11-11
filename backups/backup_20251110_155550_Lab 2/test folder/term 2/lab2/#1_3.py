import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLCDNumber, QLabel, QHBoxLayout, QVBoxLayout, QListWidget
class MyNotes(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 300, 300)
        self.setWindowTitle('Записная книжка')
        
        self.labelName = QLabel(self)
        self.labelName.setText("Имя: ")
        self.contactName = QLineEdit(self)
        
        self.labelNumber = QLabel(self)
        self.labelNumber.setText("Телефон: ")
        self.contactNumber = QLineEdit(self)
        
        self.btnAdd = QPushButton('Добавить', self)
        self.btnAdd.clicked.connect(self.addToList)
        
        self.btnAdd.resize(100, 100)
        self.listWidget = QListWidget(self)
        
        name = QHBoxLayout()
        name.addWidget(self.labelName)
        name.addWidget(self.contactName)
        
        number = QHBoxLayout()
        number.addWidget(self.labelNumber)
        number.addWidget(self.contactNumber)

        
        vbox = QVBoxLayout()
        vbox.addLayout(name) 
        vbox.addLayout(number)
        
        vboxBtn = QHBoxLayout()
        vboxBtn.addLayout(vbox)
        vboxBtn.addWidget(self.btnAdd)
        
        mainBox = QVBoxLayout()
        mainBox.addLayout(vboxBtn)
        mainBox.addWidget(self.listWidget)
        self.setLayout(mainBox)
        
    def addToList(self):
        name = self.contactName.text()
        number = self.contactNumber.text()
        if name and number:
            text = f"{name} - {number}"
            self.listWidget.addItem(text)
            self.contactName.clear()
            self.contactNumber.clear()  
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyNotes()
    ex.show()
    sys.exit(app.exec())