from PyQt5 import QtWidgets

class AgentConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurer les agents")
        self.agent1 = QtWidgets.QComboBox()
        self.agent2 = QtWidgets.QComboBox()
        self.agent1.addItems(["greedy","random","llm"])
        self.agent2.addItems(["random","greedy","llm"])
        self.nb = QtWidgets.QSpinBox(); self.nb.setRange(1,1000); self.nb.setValue(20)
        form = QtWidgets.QFormLayout()
        form.addRow("Agent A1", self.agent1)
        form.addRow("Agent A2", self.agent2)
        form.addRow("Nombre de parties", self.nb)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept); btns.rejected.connect(self.reject)
        lay = QtWidgets.QVBoxLayout(self); lay.addLayout(form); lay.addWidget(btns)

    def values(self):
        return self.agent1.currentText(), self.agent2.currentText(), int(self.nb.value())
