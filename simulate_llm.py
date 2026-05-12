import csv
from agents.llm_local import LLMAgent
from tournament.manager import run_match_agents

def simulate_llm_vs_llm(prompt1, prompt2, games=20, output_csv="data/exports/llm_results.csv"):
    a1 = LLMAgent("LLM_A1", prompt=prompt1)
    a2 = LLMAgent("LLM_A2", prompt=prompt2)

    results = run_match_agents(a1, a2, games=games)

    # Sauvegarde CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Game", "A1_total", "A2_total", "Winner"])
        for i, (t1, t2) in enumerate(results["totals"], 1):
            if t1 > t2:
                winner = "A1"
            elif t2 > t1:
                winner = "A2"
            else:
                winner = "Draw"
            writer.writerow([i, t1, t2, winner])

    print(f"Simulation terminée : {games} parties jouées.")
    print(f"Résultats exportés dans {output_csv}")
    print(f"Résumé : {results}")

if __name__ == "__main__":
    simulate_llm_vs_llm(
        prompt1="Tu es un joueur débutant, tu choisis souvent au hasard.",
        prompt2="Tu es un joueur expert, tu optimises toujours tes choix.",
        games=20
    )
