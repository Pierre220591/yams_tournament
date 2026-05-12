import os, sys, inspect, importlib.util
from PyQt5 import QtWidgets
try:
    from PyQt5.QtCore import pyqtSignal
    QtWidgets.pyqtSignal = pyqtSignal
except Exception:
    pass

ROOT = os.path.abspath(os.path.dirname(__file__))
SKIP = {'.venv','venv','.git','__pycache__','build','dist'}

def py_files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP and not d.startswith('.')]
        for fn in fns:
            if fn.endswith('.py') and fn not in ('run.py','run_select.py'):
                yield os.path.join(dp, fn)

def import_by_path(p):
    name = "_mod_" + str(abs(hash(os.path.relpath(p, ROOT))))
    spec = importlib.util.spec_from_file_location(name, p)
    if not spec or not spec.loader: return None
    try:
        m = importlib.util.module_from_spec(spec)
        sys.modules[name] = m
        spec.loader.exec_module(m)
        return m
    except Exception:
        return None

cands = []
for p in py_files(ROOT):
    m = import_by_path(p)
    if not m: 
        continue
    for nm, obj in inspect.getmembers(m, inspect.isclass):
        try:
            if issubclass(obj, QtWidgets.QWidget) and obj is not QtWidgets.QWidget:
                kind = "QMainWindow" if issubclass(obj, QtWidgets.QMainWindow) else ("QDialog" if issubclass(obj, QtWidgets.QDialog) else "QWidget")
                score = (100 if kind=="QMainWindow" else 50 if kind=="QWidget" else 10)
                ln = nm.lower()
                if any(k in ln for k in ("main","window","tournament","app","ui")): score += 20
                cands.append((score, kind, nm, obj, os.path.relpath(p, ROOT)))
        except Exception:
            pass

if not cands:
    print("Aucune classe QWidget trouvée.")
    sys.exit(1)

cands.sort(key=lambda t: t[0], reverse=True)
print("Candidats détectés:")
for i,(score, kind, nm, _, path) in enumerate(cands, 1):
    print(f"{i:2d}. {nm:30s}  [{kind}]  ({path})  score={score}")

auto = next((i for i,(s,k,_,_,_) in enumerate(cands) if k=="QMainWindow"), None)
if auto is None:
    auto = 0  # premier de la liste

choice = input(f"Saisis le numéro à lancer [défaut {auto+1}]: ").strip()
idx = int(choice)-1 if choice else auto
idx = max(0, min(idx, len(cands)-1))
sel = cands[idx]
print(f"Lancement de {sel[2]} [{sel[1]}] depuis {sel[4]}")

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
w = sel[3]()
w.show()
sys.exit(app.exec_())
