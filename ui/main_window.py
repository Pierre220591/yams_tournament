from pathlib import Path
import random
from typing import List, Dict
from PyQt5 import QtWidgets, QtCore, QtGui
from core.scoring import CATEGORIES, points_for_all, score_category
from core.probabilities import next_roll_probabilities

DIE_STYLE = """
QPushButton {
  font-size: 20px; font-weight: 600; min-width: 56px; min-height: 56px;
  border: 2px solid #888; border-radius: 8px; background: #fafafa;
}
QPushButton:checked {
  background: #ffebe6; border-color: #e26b5d;
}
"""

class Player:
    def __init__(self, name: str):
        self.name = name
        self.scores: Dict[str, int] = {cat: None for cat in CATEGORIES}
    def is_complete(self) -> bool:
        return all(v is not None for v in self.scores.values())
    def total(self) -> int:
        return sum(v or 0 for v in self.scores.values())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yams Tournament - 2 Joueurs")
        self.players = [Player("Joueur 1"), Player("Joueur 2")]
        self.active = 0
        self.dice: List[int] = [0,0,0,0,0]
        self.reroll_mask: List[bool] = [False]*5
        self.rolls_left: int = 3
        self.must_choose_category: bool = False

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QVBoxLayout(central)

        header = QtWidgets.QHBoxLayout()
        self.lbl_player = QtWidgets.QLabel("")
        self.lbl_player.setStyleSheet("font-size:18px; font-weight:700;")
        header.addWidget(self.lbl_player)
        header.addStretch(1)
        self.lbl_rolls = QtWidgets.QLabel("Lancers restants: 3")
        self.lbl_rolls.setStyleSheet("font-size:16px;")
        header.addWidget(self.lbl_rolls)
        root.addLayout(header)

        dice_row = QtWidgets.QHBoxLayout()
        self.dice_btns: List[QtWidgets.QPushButton] = []
        for _ in range(5):
            b = QtWidgets.QPushButton("-")
            b.setCheckable(True)
            b.setStyleSheet(DIE_STYLE)
            b.clicked.connect(self.on_die_toggled)
            self.dice_btns.append(b)
            dice_row.addWidget(b)
        dice_row.addStretch(1)

        side_buttons = QtWidgets.QVBoxLayout()
        self.btn_roll = QtWidgets.QPushButton("Lancer les dés")
        self.btn_roll.clicked.connect(self.on_roll_clicked)
        side_buttons.addWidget(self.btn_roll)
        self.btn_reroll = QtWidgets.QPushButton("Relancer les dés sélectionnés")
        self.btn_reroll.clicked.connect(self.on_reroll_clicked)
        side_buttons.addWidget(self.btn_reroll)
        side_buttons.addStretch(1)
        dice_row.addLayout(side_buttons)
        root.addLayout(dice_row)

        bottom = QtWidgets.QHBoxLayout()
        prob_group = QtWidgets.QGroupBox("Probabilités (prochain lancer, avec la sélection actuelle)")
        prob_layout = QtWidgets.QFormLayout(prob_group)
        self.prob_labels: Dict[str, QtWidgets.QLabel] = {}
        for name in ["Yams","Carré","Brelan","Full","Petite Suite","Grande Suite"]:
            lbl = QtWidgets.QLabel("—")
            self.prob_labels[name] = lbl
            prob_layout.addRow(QtWidgets.QLabel(name+":"), lbl)
        bottom.addWidget(prob_group, 0)

        self.table = QtWidgets.QTableWidget(len(CATEGORIES), 3)
        self.table.setHorizontalHeaderLabels(["Catégorie", "Joueur 1", "Joueur 2"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.cellClicked.connect(self.on_cell_clicked)
        for r, cat in enumerate(CATEGORIES):
            item = QtWidgets.QTableWidgetItem(cat)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(r, 0, item)
            for c in (1,2):
                it = QtWidgets.QTableWidgetItem("")
                it.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(r, c, it)
        bottom.addWidget(self.table, 1)
        root.addLayout(bottom)

        footer = QtWidgets.QHBoxLayout()
        self.lbl_tot_p1 = QtWidgets.QLabel("Total J1: 0")
        self.lbl_tot_p2 = QtWidgets.QLabel("Total J2: 0")
        for w in (self.lbl_tot_p1, self.lbl_tot_p2):
            w.setStyleSheet("font-size:16px; font-weight:600;")
        footer.addWidget(self.lbl_tot_p1)
        footer.addWidget(self.lbl_tot_p2)
        footer.addStretch(1)
        self.btn_restart = QtWidgets.QPushButton("Recommencer une partie")
        self.btn_restart.clicked.connect(self.on_restart)
        footer.addWidget(self.btn_restart)
        root.addLayout(footer)

        self.refresh_ui(initial=True)

    def active_player(self):
        return self.players[self.active]

    def dice_str(self, v: int) -> str:
        return "-" if v == 0 else str(v)

    def refresh_ui(self, initial: bool=False):
        self.lbl_player.setText(f"Au tour de: {self.active_player().name}")
        self.lbl_rolls.setText(f"Lancers restants: {self.rolls_left}")
        for i, btn in enumerate(self.dice_btns):
            btn.setText(self.dice_str(self.dice[i]))
            btn.setEnabled(any(x != 0 for x in self.dice))
            btn.setChecked(self.reroll_mask[i])

        can_first_roll = (self.rolls_left == 3 and all(v == 0 for v in self.dice))
        self.btn_roll.setEnabled(can_first_roll and not self.must_choose_category)
        self.btn_reroll.setEnabled(self.rolls_left > 0 and any(self.reroll_mask) and any(x != 0 for x in self.dice) and not self.must_choose_category)

        self.update_score_preview()
        self.update_probabilities()
        self.lbl_tot_p1.setText(f"Total J1: {self.players[0].total()}")
        self.lbl_tot_p2.setText(f"Total J2: {self.players[1].total()}")

        if self.players[0].is_complete() and self.players[1].is_complete():
            self.show_end_modal()

    def update_score_preview(self):
        for r in range(len(CATEGORIES)):
            for c in (1,2):
                it = self.table.item(r, c)
                it.setForeground(QtGui.QBrush(QtGui.QColor("#000")))
                f = it.font(); f.setBold(False); it.setFont(f)
        for r, cat in enumerate(CATEGORIES):
            v1 = self.players[0].scores[cat]
            self.table.item(r, 1).setText("" if v1 is None else str(v1))
            v2 = self.players[1].scores[cat]
            self.table.item(r, 2).setText("" if v2 is None else str(v2))
        if any(x != 0 for x in self.dice):
            preview = points_for_all(self.dice)
            col = 1 + self.active
            for r, cat in enumerate(CATEGORIES):
                if self.players[self.active].scores[cat] is None:
                    it = self.table.item(r, col)
                    it.setText(str(preview[cat]))
                    it.setForeground(QtGui.QBrush(QtGui.QColor("#666")))
                    f = it.font(); f.setBold(False); it.setFont(f)

    def update_probabilities(self):
        names = ["Yams","Carré","Brelan","Full","Petite Suite","Grande Suite"]
        if not any(x != 0 for x in self.dice) or self.rolls_left == 0:
            for k in names:
                self.prob_labels[k].setText("0 %")
            return
        probs = next_roll_probabilities(self.dice, self.reroll_mask, self.rolls_left)
        for k in names:
            p = probs.get(k, 0.0)
            self.prob_labels[k].setText(f"{p*100:.1f} %")

    def on_die_toggled(self):
        for i, b in enumerate(self.dice_btns):
            self.reroll_mask[i] = b.isChecked()
        # Recalculate whole UI so the reroll button (and preview) update
        self.refresh_ui()

    def on_roll_clicked(self):
        if not (self.rolls_left == 3 and all(v == 0 for v in self.dice)):
            return
        self.dice = [random.randint(1,6) for _ in range(5)]
        self.rolls_left = 2
        self.reroll_mask = [False]*5
        self.must_choose_category = (self.rolls_left == 0)
        self.refresh_ui()

    def on_reroll_clicked(self):
        if self.rolls_left <= 0 or not any(self.reroll_mask):
            return
        for i, sel in enumerate(self.reroll_mask):
            if sel:
                self.dice[i] = random.randint(1,6)
        self.rolls_left -= 1
        self.reroll_mask = [False]*5
        self.must_choose_category = (self.rolls_left == 0)
        self.refresh_ui()

    def on_cell_clicked(self, row: int, col: int):
        if col != (1 + self.active):
            return
        cat = CATEGORIES[row]
        if not any(x != 0 for x in self.dice):
            return
        if self.players[self.active].scores[cat] is not None:
            return
        pts = score_category(self.dice, cat)
        self.players[self.active].scores[cat] = pts
        # Changer de joueur
        self.active = 1 - self.active
        self.dice = [0,0,0,0,0]
        self.reroll_mask = [False]*5
        self.rolls_left = 3
        self.must_choose_category = False
        self.refresh_ui()

    def on_restart(self):
        for p in self.players:
            p.scores = {cat: None for cat in CATEGORIES}
        self.active = 0
        self.dice = [0,0,0,0,0]
        self.reroll_mask = [False]*5
        self.rolls_left = 3
        self.must_choose_category = False
        self.refresh_ui()

    def show_end_modal(self):
        t1, t2 = self.players[0].total(), self.players[1].total()
        if t1 > t2:
            msg = f"Victoire de {self.players[0].name} ({t1} à {t2})"
        elif t2 > t1:
            msg = f"Victoire de {self.players[1].name} ({t2} à {t1})"
        else:
            msg = f"Égalité parfaite ({t1} - {t2})"
        QtWidgets.QMessageBox.information(self, "Fin de partie", msg)
