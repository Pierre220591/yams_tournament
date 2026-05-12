import random
from agents.base import Agent

class RandomAgent(Agent):
    def choose_hold(self, dice, roll, scoresheet):
        return [i for i in range(5) if random.random() < 0.5]

    def choose_category(self, dice, available_categories):
        return random.choice(available_categories)
