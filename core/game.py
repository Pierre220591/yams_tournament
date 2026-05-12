from core.utils import roll_die

class GameState:
    def __init__(self):
        self.dice = [0,0,0,0,0]
        self.rolls_done = 0

    def new_hand(self):
        self.rolls_done = 0
        self.roll_all()

    def roll_all(self):
        self.dice = [roll_die() for _ in range(5)]
        self.rolls_done += 1
        return self.dice[:]

    def reroll_unheld(self, held_mask):
        for i in range(5):
            if not held_mask[i]:
                self.dice[i] = roll_die()
        self.rolls_done += 1
        return self.dice[:]
