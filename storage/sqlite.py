import os, sqlite3, json, datetime, random

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "yams.sqlite")

def _dict_factory(cur, row):
    return {col[0]: row[idx] for idx, col in enumerate(cur.description)}

def get_conn(db_path: str = DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = _dict_factory
    return conn

def now():
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

def ensure_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS matches(
            id INTEGER PRIMARY KEY,
            started_at TEXT,
            ended_at TEXT,
            mode TEXT,
            agent_a TEXT,
            agent_b TEXT,
            games INTEGER,
            notes TEXT
        );""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY,
            match_id INTEGER,
            game_index INTEGER,
            seed INTEGER,
            started_at TEXT,
            ended_at TEXT,
            winner TEXT,
            score_a INTEGER,
            score_b INTEGER,
            FOREIGN KEY(match_id) REFERENCES matches(id)
        );""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS rolls(
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            turn_index INTEGER,
            player TEXT,
            roll_no INTEGER,
            dice_before TEXT,
            kept_mask TEXT,
            dice_after TEXT,
            probs_json TEXT,
            ts TEXT,
            FOREIGN KEY(game_id) REFERENCES games(id)
        );""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            turn_index INTEGER,
            player TEXT,
            category TEXT,
            points INTEGER,
            dice TEXT,
            ts TEXT,
            FOREIGN KEY(game_id) REFERENCES games(id)
        );""")
        conn.commit()

def start_game(seed: int | None = None) -> int:
    ensure_db()
    with get_conn() as conn:
        c = conn.cursor()
        if seed is None:
            seed = random.randint(1, 2_000_000_000)
        c.execute("INSERT INTO games(match_id,game_index,seed,started_at) VALUES(NULL,NULL,?,?);",
                  (seed, now()))
        conn.commit()
        return c.lastrowid

def end_game(game_id: int, winner: str | None, score_a: int, score_b: int):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""UPDATE games SET ended_at=?, winner=?, score_a=?, score_b=? WHERE id=?;""",
                  (now(), winner, score_a, score_b, game_id))
        conn.commit()

def log_roll(game_id: int, turn_index: int, player: str, roll_no: int,
             dice_before, kept_mask, dice_after, probs_json=None):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""INSERT INTO rolls(game_id,turn_index,player,roll_no,
                    dice_before,kept_mask,dice_after,probs_json,ts)
                    VALUES(?,?,?,?,?,?,?,?,?);""",
                  (game_id, turn_index, player, roll_no,
                   json.dumps(dice_before), json.dumps(kept_mask),
                   json.dumps(dice_after),
                   json.dumps(probs_json) if probs_json is not None else None,
                   now()))
        conn.commit()

def log_score(game_id: int, turn_index: int, player: str, category: str, points: int, dice):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""INSERT INTO scores(game_id,turn_index,player,category,points,dice,ts)
                     VALUES(?,?,?,?,?,?,?);""",
                  (game_id, turn_index, player, category, points, json.dumps(dice), now()))
        conn.commit()
