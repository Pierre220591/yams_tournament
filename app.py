import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QStyleFactory
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
from ui.main_window import MainWindow
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    qss_path = Path(__file__).parent / 'ui' / 'styles' / 'industrial_dark.qss'
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding='utf-8'))
    w = MainWindow()
    w.setMinimumSize(1120, 700)
    def tune():
        from PyQt5.QtWidgets import QGroupBox
        for gb in w.findChildren(QGroupBox):
            lay = gb.layout()
            if lay:
                lay.setContentsMargins(12, 20, 12, 12)
                lay.setSpacing(8)
        cw = w.centralWidget()
        if cw and cw.layout():
            cw.layout().setContentsMargins(12, 12, 12, 12)
            cw.layout().setSpacing(8)
        w.adjustSize()
    QtCore.QTimer.singleShot(0, tune)
    w.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
