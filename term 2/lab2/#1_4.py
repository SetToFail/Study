import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPolygonF
from PyQt5.QtCore import QPointF

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(255, 0, 0)  
        self.a = 300
        self.k = 0.9
        self.n = 10

    def setParameters(self, a, k, n):
        self.a = a
        self.k = k
        self.n = n
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.color)

        start_x = 50
        start_y = 50  
        a = self.a

        center_x = start_x + a / 2
        center_y = start_y + a / 2

        for _ in range(self.n):
            rect = QPolygonF([
                QPointF(start_x, start_y),
                QPointF(start_x + a, start_y),
                QPointF(start_x + a, start_y + a),
                QPointF(start_x, start_y + a)
            ])
            painter.drawPolygon(rect)

            a *= self.k
            start_x = center_x - a / 2
            start_y = center_y - a / 2

class Square1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Квадрат-объектив — 1')
        self.setFixedSize(500, 500) 

        control_widget = QWidget(self)
        control_layout = QVBoxLayout(control_widget)

        self.labelA = QLabel("a:")
        self.lineEdit = QLineEdit("300")
        self.labelK = QLabel("k:")
        self.lineEdit_2 = QLineEdit("0.9")
        self.labelN = QLabel("n:")
        self.lineEdit_3 = QLineEdit("10")

        self.btn = QPushButton("Показать")
        self.btn.clicked.connect(self.drawSquares)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.labelA)
        hbox1.addWidget(self.lineEdit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.labelK)
        hbox2.addWidget(self.lineEdit_2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.labelN)
        hbox3.addWidget(self.lineEdit_3)

        control_layout.addLayout(hbox1)
        control_layout.addLayout(hbox2)
        control_layout.addLayout(hbox3)
        control_layout.addWidget(self.btn)

        self.drawing_area = DrawingArea(self)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(control_widget) 
        main_layout.addWidget(self.drawing_area)  

        main_layout.setSpacing(10)  
        main_layout.setContentsMargins(20, 20, 20, 20)  

        self.setLayout(main_layout)

    def drawSquares(self):
        a = float(self.lineEdit.text())
        k = float(self.lineEdit_2.text())
        n = int(self.lineEdit_3.text())

        self.drawing_area.setParameters(a, k, n)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Square1()
    ex.show()
    sys.exit(app.exec())