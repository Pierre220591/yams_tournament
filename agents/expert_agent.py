from collections import Counter
from agents.base import Agent
from core.scoring import score_category, CATEGORIES
from core import probabilities

class ExpertAgent(Agent):
    def choose_hold(self, dice, roll, scoresheet):
        # Stratégie probabiliste : garder les dés qui maximisent la chance
        # d'améliorer une combinaison forte (Yams, Carré, Full, Suite)
        best_keep = []
        best_prob = -1.0
        for v in set(dice):
            keep = [i for i, x in enumerate(dice) if x == v]
            # Exemple : proba d'obtenir un Yams si on garde ces dés
            prob = probabilities.probability_of_yams(len(keep), 3 - roll)
            if prob > best_prob:
                best_prob = prob
                best_keep = keep
        return best_keep

    def choose_category(self, dice, available_categories):
        best_cat = None
        best_expectation = -1
        for cat in available_categories:
            immediate = score_category(dice, cat)
            # pondération par probabilité d'amélioration
            bonus = 0
            if cat == "Yams":
                bonus = probabilities.probability_of_yams(Counter(dice).most_common(1)[0][1], 0) * 50
            elif cat == "Carré":
                bonus = probabilities.probability_of_four_kind(Counter(dice).most_common(1)[0][1], 0) * sum(dice)
            elif cat == "Full":
                bonus = probabilities.probability_of_full(dice, 0) * 25
            elif cat == "Grande Suite":
                bonus = probabilities.probability_of_large_straight(dice, 0) * 40
            expectation = immediate + bonus
            if expectation > best_expectation:
                best_expectation = expectation
                best_cat = cat
        return best_cat if best_cat else available_categories[0]
