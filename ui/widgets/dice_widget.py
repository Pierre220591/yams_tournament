from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox, QLabel, QGroupBox
from PyQt5.QtCore import pyqtSignal
import random

class DiceWidget(QGroupBox):
    selection_changed = pyqtSignal(list)
    roll_happened = pyqtSignal(list, int)

    def __init__(self, parent=None):
        super().__init__("Dés", parent)
        self.dice = [1,1,1,1,1]
        self.roll_count = 0
        self.setLayout(QVBoxLayout())
        self.row = QHBoxLayout()
        self.boxes = []
        self.labels = []
        for i in range(5):
            col = QVBoxLayout()
            lbl = QLabel("1")
            lbl.setStyleSheet("font-size: 18px;")
            chk = QCheckBox("Garder")
            chk.stateChanged.connect(self._emit_selection)
            col.addWidget(lbl)
            col.addWidget(chk)
            self.labels.append(lbl)
            self.boxes.append(chk)
            self.row.addLayout(col)
        self.layout().addLayout(self.row)
        btns = QHBoxLayout()
        self.btn_roll = QPushButton("Lancer")
        self.btn_roll.clicked.connect(self.roll)
        self.btn_reset = QPushButton("Nouveau tour")
        self.btn_reset.clicked.connect(self.reset_turn)
        btns.addWidget(self.btn_roll)
        btns.addWidget(self.btn_reset)
        self.layout().addLayout(btns)

    def reset_turn(self):
        self.roll_count = 0
        for b in self.boxes:
            b.setChecked(False)
        self.roll()

    def _emit_selection(self):
        held = [i for i,b in enumerate(self.boxes) if b.isChecked()]
        self.selection_changed.emit(held)

    def roll(self):
        if self.roll_count == 0:
            self.dice = [random.randint(1,6) for _ in range(5)]
        else:
            for i,b in enumerate(self.boxes):
                if not b.isChecked():
                    self.dice[i] = random.randint(1,6)
        self.roll_count = min(self.roll_count + 1, 3)
        for i, val in enumerate(self.dice):
            self.labels[i].setText(str(val))
        self._emit_selection()
        self.roll_happened.emit(list(self.dice), min(self.roll_count-1,2))
