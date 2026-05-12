from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from core.probabilities import probability_table, INTEREST_CATS
from core.scoring import DISPLAY_NAMES

class ProbabilityPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Probabilités (prochain lancer)", parent)
        self.setLayout(QVBoxLayout())
        self.rows = {}
        for cat in INTEREST_CATS:
            row = QHBoxLayout()
            lab = QLabel(DISPLAY_NAMES[cat])
            bar = QProgressBar()
            bar.setRange(0,100)
            val = QLabel("0%")
            row.addWidget(lab, 1)
            row.addWidget(bar, 3)
            row.addWidget(val, 0)
            self.layout().addLayout(row)
            self.rows[cat] = (bar, val)

    def update_probs(self, dice, held):
        probs = probability_table(dice, held)
        for cat, (bar, lab) in self.rows.items():
            p = probs.get(cat, 0.0)
            pct = int(round(p*100))
            bar.setValue(pct)
            lab.setText(f"{pct}%")
