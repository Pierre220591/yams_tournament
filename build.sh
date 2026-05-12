#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m PyInstaller --name "YamsTournament" --windowed --noconfirm --add-data "ui/styles.qss:ui" app.py
echo "App built at dist/YamsTournament.app"
