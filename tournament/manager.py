import csv
import os
from datetime import datetime

from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.expert_agent import ExpertAgent
from agents.beginner_agent import BeginnerAgent
from agents.llm_local import LLMAgent
from core.game import GameState
from core.scoring import CATEGORIES, score_category

AGENTS = {
    "random": lambda name: RandomAgent(name),
    "greedy": lambda name: GreedyAgent(name),
    "expert": lambda name: ExpertAgent(name),
    "beginner": lambda name: BeginnerAgent(name),
    "llm": lambda name, prompt=None: LLMAgent(name, prompt=prompt),
}

def _empty_scoresheet():
    return {cat: None for cat in CATEGORIES}

def _available_categories(sheet):
    return [c for c, v in sheet.items() if v is None]

def _total(sheet):
    return sum(v for v in sheet.values() if isinstance(v, int))

def play_full_game(a1, a2, game_id=0, csv_writer=None):
    sheets = [_empty_scoresheet(), _empty_scoresheet()]
    players = [a1, a2]
    turn_number = 0

    print(f"\n🎮 Game {game_id} begins: {a1.name} vs {a2.name}")

    for _ in range(len(CATEGORIES)):
        for pid in (0, 1):
            agent = players[pid]
            sheet = sheets[pid]
            avail = _available_categories(sheet)
            if not avail:
                continue
            turn_number += 1
            gs = GameState()
            gs.new_hand()
            print(f"\n🔁 Turn {turn_number} - {agent.name}")
            print(f"🎲 Initial dice: {gs.dice}")

            for roll_index in (1, 2):
                keep_idxs = agent.choose_hold(gs.dice[:], roll_index, sheet)
                mask = [False] * 5
                for i in keep_idxs:
                    if 0 <= i < 5:
                        mask[i] = True
                gs.reroll_unheld(mask)
                print(f"🎯 Roll {roll_index+1}: kept {keep_idxs}, new dice: {gs.dice}")

            cat = agent.choose_category(gs.dice[:], avail)
            points = score_category(gs.dice[:], cat)
            sheet[cat] = points
            print(f"🗂️ Chosen category: {cat} → +{points} points")

            if csv_writer:
                csv_writer.writerow({
                    "game_id": game_id,
                    "turn_number": turn_number,
                    "player": agent.name,
                    "roll_number": 3,
                    "dice": gs.dice[:],
                    "category": cat,
                    "score": points,
                    "agent1_name": a1.name,
                    "agent2_name": a2.name,
                    "winner_name": "",
                    "agent1_score": "",
                    "agent2_score": ""
                })

    t1, t2 = _total(sheets[0]), _total(sheets[1])
    winner = -1 if t1 == t2 else (0 if t1 > t2 else 1)
    winner_name = "Draw" if winner == -1 else players[winner].name
    print(f"\n🏁 Final score: {a1.name} = {t1}, {a2.name} = {t2}")
    print(f"🏆 Winner: {winner_name}")

    if csv_writer:
        csv_writer.writerow({
            "game_id": game_id,
            "turn_number": "END",
            "player": "SUMMARY",
            "roll_number": "",
            "dice": "",
            "category": "TOTALS",
            "score": "",
            "agent1_name": a1.name,
            "agent2_name": a2.name,
            "winner_name": winner_name,
            "agent1_score": t1,
            "agent2_score": t2
        })

    return {"A1_total": t1, "A2_total": t2, "winner": winner, "csv_path": None}

def run_match(agent1_kind="greedy", agent2_kind="random", games=10, prompt1=None, prompt2=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/exports", exist_ok=True)
    csv_path = f"data/exports/results_{timestamp}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "game_id", "turn_number", "player", "roll_number", "dice", "category", "score",
            "agent1_name", "agent2_name", "winner_name", "agent1_score", "agent2_score"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        W1 = W2 = draws = 0
        for gid in range(1, games + 1):
            a1 = AGENTS["llm"]("A1", prompt=prompt1) if agent1_kind == "llm" else AGENTS[agent1_kind]("A1")
            a2 = AGENTS["llm"]("A2", prompt=prompt2) if agent2_kind == "llm" else AGENTS[agent2_kind]("A2")
            result = play_full_game(a1, a2, game_id=gid, csv_writer=writer)
            if result["winner"] == 0:
                W1 += 1
            elif result["winner"] == 1:
                W2 += 1
            else:
                draws += 1

    return {
        "games": games,
        "A1_wins": W1,
        "A2_wins": W2,
        "draws": draws,
        "csv_path": csv_path
    }
