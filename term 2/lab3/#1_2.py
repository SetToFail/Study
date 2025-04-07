import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import os
class FileProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Обработка файла с числами")
        self.setGeometry(100, 100, 400, 200)
        self.label = QLabel("Введите имя файла:", self)
        self.entry = QLineEdit(self)
        self.process_button = QPushButton("Обработать файл", self)
        self.max_value_label = QLabel("Максимальное значение = ", self)
        self.min_value_label = QLabel("Минимальное значение = ", self)
        self.avg_value_label = QLabel("Среднее значение = ", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.process_button)
        layout.addWidget(self.max_value_label)
        layout.addWidget(self.min_value_label)
        layout.addWidget(self.avg_value_label)
        self.setLayout(layout)
        self.process_button.clicked.connect(self.process_file)
    def process_file(self):
        filename = self.entry.text()
        self.max_value_label.setText("Максимальное значение = ")
        self.min_value_label.setText("Минимальное значение = ")
        self.avg_value_label.setText("Среднее значение = ")
        if not os.path.exists(filename):
            QMessageBox.critical(self, "Error", "The file does not exist")
            return
        if os.path.getsize(filename) == 0:
            QMessageBox.critical(self, "Error", "Uncorrect data")
            return
        try:
            with open(filename, 'r') as file:
                numbers = []
                for line in file:
                    parts = line.split()
                    for part in parts:
                        try:
                            number = int(part)
                            numbers.append(number)
                        except ValueError:
                            QMessageBox.critical(self, "Error", "Uncorrect data")
                            return

                if not numbers:
                    QMessageBox.critical(self, "Error", "File empty ")
                    return
                max_value = max(numbers)
                min_value = min(numbers)
                avg_value = sum(numbers) / len(numbers)
                self.max_value_label.setText(f"Максимальное значение = {max_value}")
                self.min_value_label.setText(f"Минимальное значение = {min_value}")
                self.avg_value_label.setText(f"Среднее значение = {avg_value:.2f}")
                with open("/home/danina/Repositories/Study/term 2/lab3/out.txt", "w") as out_file:
                    out_file.write(f"Максимальное значение = {max_value}\n")
                    out_file.write(f"Минимальное значение = {min_value}\n")
                    out_file.write(f"Среднее значение = {avg_value:.2f}\n")
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"an error has occurred: {e}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileProcessorApp()
    window.show()
    sys.exit(app.exec_())