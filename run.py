import os, sys, inspect, traceback, importlib.util, runpy
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
QtWidgets.pyqtSignal = pyqtSignal

ROOT = os.path.abspath(os.path.dirname(__file__))

def py_files(root):
    skip_dirs = {'.venv','venv','__pycache__','.git','build','dist','.mypy_cache','.pytest_cache'}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in skip_dirs and not d.startswith('.')]
        for fn in fns:
            if fn.endswith('.py') and fn not in ('run.py',):
                yield os.path.join(dp, fn)

def import_by_path(path):
    name = "_yt_" + str(abs(hash(os.path.relpath(path, ROOT))))
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader: 
        return None
    try:
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        print(f"[import error] {os.path.relpath(path, ROOT)}")
        traceback.print_exc(limit=2)
        return None

def score_cls(cls, mod_path):
    s = 0
    name = cls.__name__.lower()
    mp = mod_path.lower()
    if issubclass(cls, QtWidgets.QMainWindow): s += 4
    if 'main' in name or 'window' in name or 'app' in name: s += 3
    if 'ui' in mp or 'main' in mp or 'window' in mp: s += 2
    return s

def scan_candidates():
    candidates = []
    for p in py_files(ROOT):
        m = import_by_path(p)
        if not m: 
            continue
        # try a main() that returns a QWidget
        if hasattr(m, 'main') and callable(m.main):
            try:
                w = m.main()
                if isinstance(w, QtWidgets.QWidget):
                    return w
            except TypeError:
                try:
                    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
                    w = m.main(app)
                    if isinstance(w, QtWidgets.QWidget):
                        return w
                except Exception:
                    pass
            except Exception:
                pass
        # collect QWidget subclasses
        for _, obj in inspect.getmembers(m, inspect.isclass):
            try:
                if issubclass(obj, QtWidgets.QWidget) and obj is not QtWidgets.QWidget:
                    candidates.append((score_cls(obj, p), obj, p))
            except Exception:
                pass
        # factory functions
        for name in ('create_window','create_main_window','build_ui','make_window'):
            f = getattr(m, name, None)
            if callable(f):
                try:
                    w = f()
                    if isinstance(w, QtWidgets.QWidget):
                        return w
                except Exception:
                    pass
    if candidates:
        candidates.sort(key=lambda t: t[0], reverse=True)
        _, cls, p = candidates[0]
        print(f"[picked] {cls.__name__} from {os.path.relpath(p, ROOT)}")
        try:
            return cls()
        except Exception:
            traceback.print_exc(limit=2)
    return None

def find_ui():
    ui_files = []
    for dp, _, fns in os.walk(ROOT):
        for fn in fns:
            if fn.endswith('.ui'):
                ui_files.append(os.path.join(dp, fn))
    if not ui_files:
        return None
    # prefer names with main/window/app
    def ui_score(path):
        n = os.path.basename(path).lower()
        s = 0
        if 'main' in n or 'window' in n or 'app' in n: s += 2
        s += os.path.getsize(path) / 100000.0
        return s
    ui_files.sort(key=ui_score, reverse=True)
    path = ui_files[0]
    try:
        w = QtWidgets.QMainWindow()
        uic.loadUi(path, w)
        print(f"[ui] loaded {os.path.relpath(path, ROOT)}")
        return w
    except Exception:
        traceback.print_exc(limit=2)
        return None

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    w = scan_candidates()
    if not w:
        w = find_ui()
    if not w:
        w = QtWidgets.QMainWindow()
        w.setWindowTitle("Yams Tournament")
        w.resize(1000, 700)
    if isinstance(w, QtWidgets.QMainWindow):
        if not w.centralWidget():
            c = QtWidgets.QWidget()
            w.setCentralWidget(c)
    w.show()
    sys.exit(app.exec_())
