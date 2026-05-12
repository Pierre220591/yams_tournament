import csv, os
from storage.sqlite import get_conn, DB_PATH

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exports")
os.makedirs(OUT_DIR, exist_ok=True)

with get_conn(DB_PATH) as conn:
    # games
    rows = conn.execute("SELECT * FROM games ORDER BY id;").fetchall()
    with open(os.path.join(OUT_DIR, "games.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["id"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # rolls
    rows = conn.execute("SELECT * FROM rolls ORDER BY id;").fetchall()
    with open(os.path.join(OUT_DIR, "rolls.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["id"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

print("Export -> data/exports/games.csv & rolls.csv")
