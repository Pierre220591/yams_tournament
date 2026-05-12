from collections import Counter
from itertools import product
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Dice = List[int]

def _counts(d: Sequence[int]) -> Counter:
    return Counter(d)

def _is_yahtzee(d: Sequence[int]) -> bool:
    return len(set(d)) == 1

def _is_four_kind_atleast(d: Sequence[int]) -> bool:
    return max(_counts(d).values()) >= 4

def _is_three_kind_atleast(d: Sequence[int]) -> bool:
    return max(_counts(d).values()) >= 3

def _is_full_house_exact(d: Sequence[int]) -> bool:
    vals = sorted(_counts(d).values())
    return vals == [2, 3]

def _is_large_straight(d: Sequence[int]) -> bool:
    s: Set[int] = set(d)
    return s == {1,2,3,4,5} or s == {2,3,4,5,6}

def _is_small_straight_inclusive(d: Sequence[int]) -> bool:
    s: Set[int] = set(d)
    return (
        {1,2,3,4}.issubset(s)
        or {2,3,4,5}.issubset(s)
        or {3,4,5,6}.issubset(s)
    )

def _iter_next_rolls(current: Sequence[int], held_indices: Sequence[int]) -> Iterable[Dice]:
    current = list(current)
    held = set(int(i) for i in held_indices)
    free_slots = [i for i in range(5) if i not in held]
    if not free_slots:
        yield current[:]
        return
    for rolls in product(range(1,7), repeat=len(free_slots)):
        d = current[:]
        for pos, val in zip(free_slots, rolls):
            d[pos] = val
        yield d

def compute_probabilities(current: Sequence[int], held_indices: Sequence[int]) -> Dict[str, float]:
    """
    Calcule les probabilités (prochain lancer) en tenant compte des dés gardés.
    Renvoie un dict de clés:
      - "brelan" (>=3 identiques)
      - "carre" (>=4 identiques)
      - "full" (exactement 3+2)
      - "petite_suite" (suite de 4 inclut grande)
      - "grande_suite" (suite de 5)
      - "yams" (5 identiques)
    Les valeurs sont des probabilités entre 0.0 et 1.0.
    """
    total_free = 5 - len(set(int(i) for i in held_indices))
    total = 6 ** total_free if total_free >= 0 else 0
    if total == 0:
        return {k: 0.0 for k in ["brelan","carre","full","petite_suite","grande_suite","yams"]}

    counts = {
        "brelan": 0,
        "carre": 0,
        "full": 0,
        "petite_suite": 0,
        "grande_suite": 0,
        "yams": 0,
    }
    for d in _iter_next_rolls(current, held_indices):
        if _is_three_kind_atleast(d): counts["brelan"] += 1
        if _is_four_kind_atleast(d): counts["carre"] += 1
        if _is_full_house_exact(d): counts["full"] += 1
        if _is_small_straight_inclusive(d): counts["petite_suite"] += 1
        if _is_large_straight(d): counts["grande_suite"] += 1
        if _is_yahtzee(d): counts["yams"] += 1

    return {k: counts[k] / total for k in counts}

def compute_percentages(current: Sequence[int], held_indices: Sequence[int]) -> Dict[str, int]:
    """
    Renvoie les mêmes clés que compute_probabilities, mais en pourcentages entiers arrondis.
    """
    probs = compute_probabilities(current, held_indices)
    return {k: int(round(v * 100)) for k, v in probs.items()}

if __name__ == "__main__":
    # Test rapide en ligne de commande
    import sys, json
    # Exemple: python tournament/probabilities.py "[2,3,1,5,3]" "[]"
    cur = json.loads(sys.argv[1]) if len(sys.argv) > 1 else [2,3,1,5,3]
    held = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
    print(json.dumps({
        "probs": compute_probabilities(cur, held),
        "percents": compute_percentages(cur, held)
    }, indent=2, sort_keys=True))
