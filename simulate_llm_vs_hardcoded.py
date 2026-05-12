from agents.llm_local import LLMAgent
from agents.hardcoded_agent import HardcodedAgent
from core.game import GameState
from core.scoring import CATEGORIES, score_category

def play_one_game(llm_prompt):
    a1 = LLMAgent("LLM_A1", prompt=llm_prompt)
    a2 = HardcodedAgent("Hardcoded_A2")
    players = [a1, a2]
    sheets = [{cat: None for cat in CATEGORIES} for _ in range(2)]

    for turn in range(len(CATEGORIES)):
        for pid, agent in enumerate(players):
            sheet = sheets[pid]
            avail = [c for c, v in sheet.items() if v is None]
            if not avail:
                continue

            gs = GameState()
            gs.new_hand()

            # --- Phase de lancers ---
            for roll_index in (0, 1, 2):
                if isinstance(agent, LLMAgent):
                    print(f"\n[LLM] Tour {turn+1}, Joueur {agent.name}, Lancer {roll_index+1}")
                keep_idxs = agent.choose_hold(gs.dice[:], roll_index, sheet)
                if isinstance(agent, LLMAgent):
                    print(f"[LLM] Dés actuels: {gs.dice} → garde indices {keep_idxs}")
                mask = [False] * 5
                for i in keep_idxs:
                    if 0 <= i < 5:
                        mask[i] = True
                if roll_index < 2:
                    gs.reroll_unheld(mask)

            # --- Choix de catégorie ---
            if isinstance(agent, LLMAgent):
                print(f"[LLM] Dés finaux: {gs.dice}, Catégories possibles: {avail}")
            cat = agent.choose_category(gs.dice[:], avail)
            if isinstance(agent, LLMAgent):
                print(f"[LLM] Choisit la catégorie: {cat}")
            if cat not in avail:
                cat = avail[0]
            sheet[cat] = score_category(gs.dice[:], cat)

    t1 = sum(v for v in sheets[0].values() if isinstance(v, int))
    t2 = sum(v for v in sheets[1].values() if isinstance(v, int))

    print("\n=== Résultat final ===")
    print(f"LLM_A1 total: {t1}")
    print(f"Hardcoded_A2 total: {t2}")
    if t1 > t2:
        print("Victoire du LLM 🎉")
    elif t2 > t1:
        print("Victoire du Hardcoded 🤖")
    else:
        print("Égalité parfaite !")

if __name__ == "__main__":
    for i in range(3):
        print(f"\n=== Partie {i+1} ===")
        play_one_game("Tu es un joueur de Yams. Essaie de maximiser ton score intelligemment.")
