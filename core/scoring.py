from collections import Counter
from typing import Dict, List

CATEGORIES = [
    "As", "Deux", "Trois", "Quatre", "Cinq", "Six",
    "Brelan", "Carré", "Full", "Petite Suite", "Grande Suite", "Yams", "Chance"
]

def _has_n_of_a_kind(dice: List[int], n: int) -> bool:
    c = Counter(dice)
    return any(v >= n for v in c.values())

def _is_full(dice: List[int]) -> bool:
    c = sorted(Counter(dice).values(), reverse=True)
    return c[:2] == [3, 2]

def _is_small_straight(dice: List[int]) -> bool:
    s = set(dice)
    return ({1,2,3,4}.issubset(s) or {2,3,4,5}.issubset(s) or {3,4,5,6}.issubset(s))

def _is_large_straight(dice: List[int]) -> bool:
    s = set(dice)
    return s == {1,2,3,4,5} or s == {2,3,4,5,6}

def is_yams(dice: List[int]) -> bool:
    return _has_n_of_a_kind(dice, 5)

def is_four_kind(dice: List[int]) -> bool:
    return _has_n_of_a_kind(dice, 4)

def is_three_kind(dice: List[int]) -> bool:
    return _has_n_of_a_kind(dice, 3)

def is_full_house(dice: List[int]) -> bool:
    return _is_full(dice)

def is_small_straight(dice: List[int]) -> bool:
    return _is_small_straight(dice)

def is_large_straight(dice: List[int]) -> bool:
    return _is_large_straight(dice)

FULL_POINTS = 25
SMALL_STRAIGHT_POINTS = 30
LARGE_STRAIGHT_POINTS = 40
YAMS_POINTS = 50

def score_category(dice: List[int], category: str) -> int:
    dice = list(dice)
    if category == "As":
        return sum(v for v in dice if v == 1)
    if category == "Deux":
        return sum(v for v in dice if v == 2)
    if category == "Trois":
        return sum(v for v in dice if v == 3)
    if category == "Quatre":
        return sum(v for v in dice if v == 4)
    if category == "Cinq":
        return sum(v for v in dice if v == 5)
    if category == "Six":
        return sum(v for v in dice if v == 6)
    if category == "Brelan":
        return sum(dice) if is_three_kind(dice) else 0
    if category == "Carré":
        return sum(dice) if is_four_kind(dice) else 0
    if category == "Full":
        return FULL_POINTS if is_full_house(dice) else 0
    if category == "Petite Suite":
        return SMALL_STRAIGHT_POINTS if is_small_straight(dice) else 0
    if category == "Grande Suite":
        return LARGE_STRAIGHT_POINTS if is_large_straight(dice) else 0
    if category == "Yams":
        return YAMS_POINTS if is_yams(dice) else 0
    if category == "Chance":
        return sum(dice)
    raise ValueError(f"Catégorie inconnue: {category}")

def points_for_all(dice: List[int]) -> Dict[str, int]:
    return {cat: score_category(dice, cat) for cat in CATEGORIES}
