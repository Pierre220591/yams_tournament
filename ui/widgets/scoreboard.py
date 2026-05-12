from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class Scoreboard(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 6, parent)
        self.setHorizontalHeaderLabels(["Agent","Parties","Victoires","Nuls","Défaites","+/-"])
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)

    def update_from_stats(self, stats):
        self.setRowCount(0)
        for name, s in stats.items():
            row = self.rowCount()
            self.insertRow(row)
            diff = s["points_for"] - s["points_against"]
            items = [
                QTableWidgetItem(name),
                QTableWidgetItem(str(s["games"])),
                QTableWidgetItem(str(s["wins"])),
                QTableWidgetItem(str(s["draws"])),
                QTableWidgetItem(str(s["losses"])),
                QTableWidgetItem(str(diff)),
            ]
            for i, it in enumerate(items):
                it.setTextAlignment(Qt.AlignCenter)
                self.setItem(row, i, it)
        self.resizeColumnsToContents()
