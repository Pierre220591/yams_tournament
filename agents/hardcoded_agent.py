from collections import Counter
from agents.base import Agent
from core.scoring import score_category, CATEGORIES

class HardcodedAgent(Agent):
    def __init__(self, name):
        self.name = name
        self.low_categories = ["As", "Deux", "Trois", "Quatre", "Cinq", "Six"]

    def choose_hold(self, dice, roll_index, scoresheet):
        counts = Counter(dice)
        # Cherche la valeur la plus fréquente
        v, c = counts.most_common(1)[0]
        # Garde tous les dés de cette valeur
        return [i for i, x in enumerate(dice) if x == v]

    def choose_category(self, dice, available_categories):
        # Évalue le score potentiel de chaque catégorie
        best_cat = None
        best_score = -1
        for cat in available_categories:
            val = score_category(dice, cat)
            if val > best_score:
                best_score = val
                best_cat = cat

        if best_score > 0:
            return best_cat

        # Sinon, consomme une petite catégorie (1,2,3…)
        for cat in self.low_categories:
            if cat in available_categories:
                return cat

        # Fallback
        return available_categories[0]
