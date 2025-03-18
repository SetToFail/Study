import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import math

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Красивый калькулятор')
        self.setGeometry(100, 100, 300, 400)

        self.display = QLineEdit(self)
        self.display.setFont(QFont('Arial', 80))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        grid = QGridLayout()
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', '*',
            '0', '.', '=', '/',
            '^', '√', '!', 'C'
        ]

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, button in zip(positions, buttons):
            btn = QPushButton(button)
            btn.setFont(QFont('Arial', 16))
            btn.setFixedSize(60, 60)
            if button == 'C':
                btn.setStyleSheet("background-color: orange; color: black;")
            btn.clicked.connect(self.onClick)
            grid.addWidget(btn, *position)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def onClick(self):
        button = self.sender()
        text = button.text()

        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', 'Невозможно вычислить выражение')
        elif text == '√':
            try:
                value = float(self.display.text())
                if value < 0:
                    raise ValueError
                self.display.setText(str(math.sqrt(value)))
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Квадратный корень из отрицательного числа')
        elif text == '^':
            self.display.setText(self.display.text() + '**')
        elif text == '!':
            try:
                value = int(self.display.text())
                if value < 0:
                    raise ValueError
                self.display.setText(str(math.factorial(value)))
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Факториал определён только для неотрицательных целых чисел')
        else:
            self.display.setText(self.display.text() + text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())