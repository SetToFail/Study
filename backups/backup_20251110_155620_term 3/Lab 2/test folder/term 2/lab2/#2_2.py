import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class RandomFlag(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('Random Flag')

        self.color = QColor(255, 255, 255)
        self.num_colors = 3
        self.base = [50, 50, 200, 30]

        self.button = QPushButton('Создать флаг', self)
        self.button.clicked.connect(self.generateFlag)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    def generateFlag(self):
        num_colors, ok = QInputDialog.getInt(self, 'Количество цветов', 'Введите количество цветов (1-10):', 3, 1, 10, 1)
        if ok:
            self.num_colors = num_colors
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        x, y, width, height = self.base

        for i in range(self.num_colors):
            r = random.randrange(0, 256)
            g = random.randrange(0, 256)
            b = random.randrange(0, 256)
            color = QColor(r, g, b)

            painter.fillRect(x, y + i * height, width, height, color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RandomFlag()
    ex.show()
    sys.exit(app.exec())