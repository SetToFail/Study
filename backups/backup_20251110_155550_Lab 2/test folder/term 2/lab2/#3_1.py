import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QMouseEvent

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Убегающая кнопка')
        self.setGeometry(100, 100, 800, 600)

        self.button = QPushButton('button', self)
        self.button.setFixedSize(100, 50)
        self.button.move(350, 250)  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkMousePosition)
        self.timer.start(10)  

    def checkMousePosition(self):
        mouse_pos = self.mapFromGlobal(self.cursor().pos())

        button_rect = self.button.geometry()

        if button_rect.contains(mouse_pos):
            new_x = button_rect.x()
            new_y = button_rect.y()

            if mouse_pos.x() > button_rect.center().x():
                new_x -= 20  
            else:
                new_x += 20  

            if mouse_pos.y() > button_rect.center().y():
                new_y -= 20  
            else:
                new_y += 20  

            new_x = max(0, min(new_x, self.width() - button_rect.width()))
            new_y = max(0, min(new_y, self.height() - button_rect.height()))

            self.button.move(new_x, new_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())