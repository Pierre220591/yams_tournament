import random
from collections import Counter
from agents.base import Agent
from core.scoring import score_category, CATEGORIES

class BeginnerAgent(Agent):
    """
    Agent risqué : vise le spectaculaire (Yams, Carré, Full, Suites),
    relance agressivement, et sacrifie souvent des catégories.
    """

    def choose_hold(self, dice, roll, scoresheet):
        # Si main vide (début du tour)
        if not dice:
            return []

        counts = Counter(dice)
        val, freq = counts.most_common(1)[0]

        # Si proche d'une combinaison forte : garder les dés identiques
        if freq >= 3:
            return [i for i, v in enumerate(dice) if v == val]

        # Sinon : comportement risqué → garder très peu de dés 
        nb_to_keep = random.choice([0, 1, 2])  # agressif
        indices = list(range(5))
        random.shuffle(indices)
        return sorted(indices[:nb_to_keep])

    def choose_category(self, dice, available_categories):
        # Score immédiat par catégorie
        scores = {cat: score_category(dice, cat) for cat in available_categories}

        # 1️⃣ Si une combinaison forte donne un score > 0 → la choisir
        big_cats = ["Yams", "Carré", "Full", "Grande Suite", "Petite Suite"]
        scored_big = [(cat, s) for cat, s in scores.items() if s > 0 and cat in big_cats]
        if scored_big:
            return max(scored_big, key=lambda x: x[1])[0]

        # 2️⃣ Sinon, choisir la meilleure catégorie restante selon score immédiat
        if any(s > 0 for s in scores.values()):
            return max(scores.items(), key=lambda x: x[1])[0]

        # 3️⃣ Si tout est nul → sacrifier une catégorie "faible" 
        weak_cats = [c for c in available_categories if c not in big_cats]
        return random.choice(weak_cats) if weak_cats else random.choice(available_categories)
