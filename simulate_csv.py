import csv
from tournament.manager import run_match

def main():
    # On lance 200 parties entre Random et Greedy
    results = run_match("random", "greedy", games=200)

    # Écriture dans un CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Game", "A1_total", "A2_total", "Winner"])
        for i, (t1, t2) in enumerate(results["totals"], start=1):
            if t1 > t2:
                winner = "A1"
            elif t2 > t1:
                winner = "A2"
            else:
                winner = "Draw"
            writer.writerow([i, t1, t2, winner])

    print("Simulation terminée ✅")
    print(f"Résumé : {results}")
    print("Les résultats détaillés sont dans results.csv")

if __name__ == "__main__":
    main()
