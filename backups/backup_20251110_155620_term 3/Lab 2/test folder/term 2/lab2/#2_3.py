import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect

class GoodMoodRising(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 1000)
        self.setWindowTitle('GoodMoodRising')

        self.color = QColor(0, 0, 0)

        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setGeometry(970, 40, 20, 500)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.color)

        size = self.slider.value()

        big_square_size = 10 * size
        painter.drawEllipse(0, 0, big_square_size, big_square_size)

        eye_size = 2 * size
        left_eye_x = 2 * size
        left_eye_y = 2 * size
        painter.drawEllipse(left_eye_x, left_eye_y, eye_size, eye_size)

        right_eye_x = big_square_size - 4 * size
        right_eye_y = 2 * size
        painter.drawEllipse(right_eye_x, right_eye_y, eye_size, eye_size)

        smile_x = 2 * size
        smile_y = 6 * size
        smile_width = 6 * size
        smile_height = 2 * size
        painter.drawArc(smile_x, smile_y, smile_width, smile_height, -480, -1920)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GoodMoodRising()
    ex.show()
    sys.exit(app.exec())