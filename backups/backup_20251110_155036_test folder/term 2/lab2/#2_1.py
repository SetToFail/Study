import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPolygonF
from PyQt5.QtCore import QPointF

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(255, 0, 0)
        self.k = 0.8
        self.n = 20

    def setParameters(self, k, n):
        self.k = k
        self.n = n
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.color)

        start_x = 125
        start_y = 0
        side = 200

        points = [
            QPointF(start_x, start_y),
            QPointF(start_x + side, start_y),
            QPointF(start_x + side, start_y + side),
            QPointF(start_x, start_y + side)
        ]

        for _ in range(self.n):
            polygon = QPolygonF(points)
            painter.drawPolygon(polygon)

            new_points = []
            for i in range(4):
                x1 = points[i].x()
                y1 = points[i].y()
                x2 = points[(i + 1) % 4].x()
                y2 = points[(i + 1) % 4].y()

                new_x = x1 + (x2 - x1) * self.k
                new_y = y1 + (y2 - y1) * self.k
                new_points.append(QPointF(new_x, new_y))

            points = new_points

class Square2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Квадрат-объектив — 2')
        self.setFixedSize(500, 500)

        control_widget = QWidget(self)
        control_layout = QVBoxLayout(control_widget)

        self.labelK = QLabel("k:")
        self.k = QLineEdit("0.8")
        self.labelN = QLabel("n:")
        self.n = QLineEdit("20")

        self.draw = QPushButton("Рисовать")
        self.draw.clicked.connect(self.drawSquares)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.labelK)
        hbox1.addWidget(self.k)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.labelN)
        hbox2.addWidget(self.n)

        control_layout.addLayout(hbox1)
        control_layout.addLayout(hbox2)
        control_layout.addWidget(self.draw)

        self.drawing_area = DrawingArea(self)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(control_widget)
        main_layout.addWidget(self.drawing_area)

        main_layout.setSpacing(10) 
        main_layout.setContentsMargins(20, 20, 20, 20)  

        self.setLayout(main_layout)

    def drawSquares(self):
        k = float(self.k.text())
        n = int(self.n.text())

        self.drawing_area.setParameters(k, n)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Square2()
    ex.show()
    sys.exit(app.exec())