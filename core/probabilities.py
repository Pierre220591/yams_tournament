from itertools import product
from typing import Dict, List
from core.scoring import (
    is_yams, is_four_kind, is_three_kind,
    is_full_house, is_large_straight, is_small_straight
)

def next_roll_probabilities(dice: List[int], reroll_mask: List[bool], rolls_left: int = 1) -> Dict[str, float]:
    assert len(dice) == 5 and len(reroll_mask) == 5, "5 dés et 5 booléens requis"
    n = sum(1 for b in reroll_mask if b)
    if rolls_left <= 0 or n == 0:
        return {k: 0.0 for k in ["Yams","Carré","Brelan","Full","Petite Suite","Grande Suite"]}
    idx = [i for i, b in enumerate(reroll_mask) if b]
    total = 6 ** n
    hit = {k: 0 for k in ["Yams","Carré","Brelan","Full","Petite Suite","Grande Suite"]}
    base = list(dice)
    for outcome in product(range(1,7), repeat=n):
        final = base[:]
        for pos, val in zip(idx, outcome):
            final[pos] = val
        if is_yams(final): hit["Yams"] += 1
        if is_four_kind(final): hit["Carré"] += 1
        if is_three_kind(final): hit["Brelan"] += 1
        if is_full_house(final): hit["Full"] += 1
        if is_small_straight(final): hit["Petite Suite"] += 1
        if is_large_straight(final): hit["Grande Suite"] += 1
    return {k: hit[k] / total for k in hit.keys()}
import math
from collections import Counter

def probability_of_yams(kept: int, rolls_left: int) -> float:
    """
    Approximation de la probabilité d'obtenir un Yams
    kept = nombre de dés identiques déjà gardés
    rolls_left = nombre de relances restantes
    """
    needed = 5 - kept
    if needed <= 0:
        return 1.0
    if rolls_left <= 0:
        return 0.0
    # probabilité d'obtenir les dés manquants en rolls_left essais
    p_single = (1/6) ** needed
    return min(1.0, rolls_left * p_single)

def probability_of_four_kind(kept: int, rolls_left: int) -> float:
    """
    Probabilité approximative d'obtenir un Carré
    kept = nombre de dés identiques déjà gardés
    """
    needed = 4 - kept
    if needed <= 0:
        return 1.0
    if rolls_left <= 0:
        return 0.0
    p_single = (1/6) ** needed
    return min(1.0, rolls_left * p_single)

def probability_of_full(dice, rolls_left: int) -> float:
    """
    Approximation pour le Full : si on a déjà un brelan ou une paire,
    on estime la chance de compléter.
    """
    c = Counter(dice)
    if 3 in c.values() and 2 in c.values():
        return 1.0
    if 3 in c.values():
        return 0.5 if rolls_left > 0 else 0.0
    if list(c.values()).count(2) >= 2:
        return 0.5 if rolls_left > 0 else 0.0
    if 2 in c.values():
        return 0.3 if rolls_left > 0 else 0.0
    return 0.1 if rolls_left > 0 else 0.0

def probability_of_large_straight(dice, rolls_left: int) -> float:
    """
    Approximation pour la Grande Suite (1-5 ou 2-6).
    """
    s = set(dice)
    if s == {1,2,3,4,5} or s == {2,3,4,5,6}:
        return 1.0
    if rolls_left <= 0:
        return 0.0
    # si on a déjà 4 dés consécutifs
    if {1,2,3,4}.issubset(s) or {2,3,4,5}.issubset(s) or {3,4,5,6}.issubset(s):
        return 0.5
    # si on a 3 dés consécutifs
    if {1,2,3}.issubset(s) or {2,3,4}.issubset(s) or {3,4,5}.issubset(s) or {4,5,6}.issubset(s):
        return 0.3
    return 0.1
