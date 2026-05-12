from collections import Counter
from agents.base import Agent
from core.scoring import score_category

class GreedyAgent(Agent):
    def choose_hold(self, dice, roll, scoresheet):
        if not dice:
            return []
        v, _ = Counter(dice).most_common(1)[0]
        return [i for i, x in enumerate(dice) if x == v]

    def choose_category(self, dice, available_categories):
        best_cat = None
        best_score = -1
        for cat in available_categories:
            s = score_category(dice, cat)
            if s > best_score:
                best_score = s
                best_cat = cat
        return best_cat if best_cat is not None else available_categories[0]
