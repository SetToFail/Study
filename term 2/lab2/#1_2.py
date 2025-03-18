import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                             QRadioButton, QLabel, QVBoxLayout, QHBoxLayout, QButtonGroup)

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.current_player = "X"
        self.game_over = False
        self.init_ui()

    def init_ui(self):
        # Настройка радио-кнопок для выбора первого игрока
        self.x_radio = QRadioButton("X начинает", checked=True)
        self.o_radio = QRadioButton("O начинает")
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.x_radio)
        self.radio_group.addButton(self.o_radio)
        self.radio_group.buttonClicked.connect(self.new_game)

        # Создание игрового поля 3x3
        grid = QGridLayout()
        self.buttons = []
        for row in range(3):
            for col in range(3):
                button = QPushButton("")
                button.setFixedSize(80, 80)
                button.clicked.connect(self.make_move)
                grid.addWidget(button, row, col)
                self.buttons.append(button)

        # Элементы управления
        self.status_label = QLabel("Ход игрока: X")
        self.new_game_btn = QPushButton("Новая игра")
        self.new_game_btn.clicked.connect(self.new_game)

        # Компоновка интерфейса
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.x_radio)
        control_layout.addWidget(self.o_radio)
        control_layout.addStretch()
        control_layout.addWidget(self.new_game_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)
        main_layout.addLayout(grid)
        main_layout.addWidget(self.status_label)
        self.setLayout(main_layout)

        self.setWindowTitle("Крестики-нолики")
        self.new_game()

    def make_move(self):
        if self.game_over:
            return

        button = self.sender()
        if button.text() == "":
            button.setText(self.current_player)
            if self.check_win():
                self.status_label.setText(f"Выиграл {self.current_player}!")
                self.game_over = True
            elif self.check_draw():
                self.status_label.setText("Ничья!")
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.setText(f"Ход игрока: {self.current_player}")

    def check_win(self):
        # Проверка всех выигрышных комбинаций
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтали
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикали
            (0, 4, 8), (2, 4, 6)              # Диагонали
        ]
        for a, b, c in win_combinations:
            if (self.buttons[a].text() == self.buttons[b].text() == self.buttons[c].text() 
                and self.buttons[a].text() != ""):
                return True
        return False

    def check_draw(self):
        # Проверка на ничью
        return all(btn.text() != "" for btn in self.buttons)

    def new_game(self):
        # Сброс игры
        self.game_over = False
        self.current_player = "X" if self.x_radio.isChecked() else "O"
        for button in self.buttons:
            button.setText("")
            button.setEnabled(True)
        self.status_label.setText(f"Ход игрока: {self.current_player}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec_())