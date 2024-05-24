import random

class DiceGame:
    def __init__(self, rounds):
        self.game_finished = False
        self.max_rounds = rounds
        self.reset()

    def roll_dice(self):
        dice = [random.randint(1, 6) for _ in range(3)]
        while 6 in dice:
            dice = [random.randint(1, 6) if die == 6 else die for die in dice]
        return dice

    def calculate_score(self, dice):
        if sorted(dice) == [1, 2, 4]:
            self.game_finished = True
            return 421  # Special case: rolling 421 means an instant win
        elif dice[0] == dice[1] == dice[2]:
            return 20
        else:
            return max(dice)

    def play_round(self):
        dice = self.roll_dice()
        round_score = self.calculate_score(dice)
        self.total_score += round_score
        self.round_count += 1
        if self.total_score == 421 or self.round_count >= self.max_rounds:
            self.game_finished = True
        return dice, round_score, self.game_finished

    def reset(self):
        self.total_score = 0
        self.round_count = 0
        self.game_finished = False
