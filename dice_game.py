import random

class DiceGame:
    def __init__(self, rounds):
        self.total_score = 0
        self.round_score = 0
        self.round_count = 0
        self.max_rounds = rounds
        self.game_over = False

    def roll_dice(self):
        return [random.randint(1, 6) for _ in range(3)]

    def calculate_score(self, dice):
        if dice == [4, 2, 1]:
            return 21
        elif dice[0] == dice[1] == dice[2]:
            return 20
        else:
            return max(dice)

    def play_round(self):
        print("\nRound", self.round_count + 1)
        input("Press Enter to roll the dice...")

        dice = self.roll_dice()
        print("You rolled:", dice)

        while True:
            if 6 in dice:
                print("At least one die showed a 6! Rerolling...")
                dice = [random.randint(1, 6) if die == 6 else die for die in dice]
                print("After rerolling, you got:", dice)
                if 6 not in dice:
                    break
            else:
                break



        if dice == [4, 2, 1]:
            print("Congratulations! You rolled 421 and won the game!")
            self.game_over = True
            return

        round_score = self.calculate_score(dice)
        print("Your score for this round is:", round_score)

        self.total_score += round_score
        print("Your total score so far is:", self.total_score)

        self.round_count += 1

    def replay(self):
        while True:
            choice = input("\nDo you want to play the round? (yes/no): ").lower()
            if choice in ("yes", "no"):
                return choice == "yes"
            else:
                print("Please enter 'yes' or 'no'.")

def main():
    while True:
        print("Welcome to the 421 Dice Game!")
        rounds = input("How many rounds do you want to play? (3/5/8): ")
        if rounds in ("3", "5", "8"):
            rounds = int(rounds)
            break
        else:
            print("Please choose 3, 5, or 8 rounds.")

    while True:
        game = DiceGame(rounds)
        while not game.game_over and game.round_count < game.max_rounds:
            game.play_round()
            if game.game_over:
                break
            if game.round_count == game.max_rounds:
                print("You have reached the maximum number of rounds.")
                break
            if not game.replay():
                break

        choice = input("Do you want to play again? (yes/no): ").lower()
        if choice != "yes":
            break

        while True:
            print("Starting a new game...")
            rounds = input("How many rounds do you want to play? (3/5/8): ")
            if rounds in ("3", "5", "8"):
                rounds = int(rounds)
                break
            else:
                print("Please choose 3, 5, or 8 rounds.")

if __name__ == "__main__":
    main()
