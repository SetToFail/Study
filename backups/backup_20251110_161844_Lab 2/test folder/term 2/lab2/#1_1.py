import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QCheckBox, QPushButton, QPlainTextEdit)
class MacOrder(QWidget):
    def __init__(self):
        super().__init__()
        self.menu_checkboxes = []
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        menu_items = ["Чизбургер", "Гамбургер", "Кока-кола", "Наггетсы"]
        for item in menu_items:
            cb = QCheckBox(item)
            self.menu_checkboxes.append(cb)
            layout.addWidget(cb)
        self.order_btn = QPushButton("Заказать")
        self.order_btn.clicked.connect(self.show_order)
        layout.addWidget(self.order_btn)
        
        self.result = QPlainTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)
        
        self.setLayout(layout)
        self.setWindowTitle('Макдональдс - Заказ')
    
    def show_order(self):
        selected_items = []
        for cb in self.menu_checkboxes:
            if cb.isChecked():
                selected_items.append(cb.text())
        order_text = "Ваш заказ:\n\n" + "\n".join(selected_items)
        self.result.setPlainText(order_text)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MacOrder()
    ex.show()
    sys.exit(app.exec_())