PY := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: venv install run build clean

venv:
	python3 -m venv .venv

install: venv
	$(PIP) install -r requirements.txt

run:
	$(PY) app.py

build:
	$(PY) -m PyInstaller \
		--name "YamsTournament" \
		--windowed \
		--noconfirm \
		--add-data "ui/styles.qss:ui" \
		app.py

clean:
	rm -rf build dist *.spec
