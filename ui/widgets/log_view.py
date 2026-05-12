from PyQt5.QtWidgets import QTextEdit

class LogView(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def log(self, msg):
        self.append(msg)
