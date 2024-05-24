import pygame
import sys
import random
from dice_class import DiceGame

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DICE_SIZE = 100
DICE_MARGIN = 20
DOT_RADIUS = 10
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
FONT_SIZE = 32
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("421 Dice Game")
font = pygame.font.SysFont(None, FONT_SIZE)


def draw_dice(dice, x, y):
    positions = {
        1: [(x + DICE_SIZE // 2, y + DICE_SIZE // 2)],
        2: [(x + DICE_MARGIN, y + DICE_MARGIN), (x + DICE_SIZE - DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN)],
        3: [(x + DICE_MARGIN, y + DICE_MARGIN), (x + DICE_SIZE // 2, y + DICE_SIZE // 2),
            (x + DICE_SIZE - DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN)],
        4: [(x + DICE_MARGIN, y + DICE_MARGIN), (x + DICE_SIZE - DICE_MARGIN, y + DICE_MARGIN),
            (x + DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN), (x + DICE_SIZE - DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN)],
        5: [(x + DICE_MARGIN, y + DICE_MARGIN), (x + DICE_SIZE - DICE_MARGIN, y + DICE_MARGIN),
            (x + DICE_SIZE // 2, y + DICE_SIZE // 2), (x + DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN),
            (x + DICE_SIZE - DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN)],
        6: [(x + DICE_MARGIN, y + DICE_MARGIN), (x + DICE_SIZE - DICE_MARGIN, y + DICE_MARGIN),
            (x + DICE_MARGIN, y + DICE_SIZE // 2), (x + DICE_SIZE - DICE_MARGIN, y + DICE_SIZE // 2),
            (x + DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN), (x + DICE_SIZE - DICE_MARGIN, y + DICE_SIZE - DICE_MARGIN)]
    }

    # Draw dice border
    pygame.draw.rect(window, BLACK, (x, y, DICE_SIZE, DICE_SIZE), 2)

    # Draw dots
    for pos in positions[dice]:
        pygame.draw.circle(window, BLACK, pos, DOT_RADIUS)


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)


def main():
    game = None
    running = True
    dice = [1, 1, 1]
    round_score = 0
    message = ""

    while running:
        window.fill(WHITE)

        if game is None:
            draw_text("Choose the number of rounds (3/5/8):", font, BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
            draw_text("Press 3, 5, or 8 to start", font, BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        game = DiceGame(4)
                        message = ""  # Reset the message when starting a new game
                    elif event.key == pygame.K_5:
                        game = DiceGame(6)
                        message = ""  # Reset the message when starting a new game
                    elif event.key == pygame.K_8:
                        game = DiceGame(9)
                        message = ""  # Reset the message when starting a new game
        elif game.game_finished:
            if game.total_score >= 421 or round_score == 421:
                draw_text(f"Game Over! Final Score: {game.total_score}", font, BLACK, WINDOW_WIDTH // 2,
                          WINDOW_HEIGHT // 2 - 50)
            else:
                draw_text(f"Game Over! Final Score: {game.total_score}", font, BLACK, WINDOW_WIDTH // 2,
                          WINDOW_HEIGHT // 2 - 50)
            reset_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, WINDOW_HEIGHT // 2, BUTTON_WIDTH,
                                       BUTTON_HEIGHT)
            pygame.draw.rect(window, BLACK, reset_button)
            draw_text("Reset Game", font, WHITE, reset_button.centerx, reset_button.centery)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_button.collidepoint(event.pos):
                        game = None  # Set game to None to go back to the round selection screen
        else:
            draw_text(f"Round {game.round_count} / {game.max_rounds - 1}", font, BLACK, WINDOW_WIDTH // 2, 50)
            draw_text(f"Total score: {game.total_score}", font, BLACK, WINDOW_WIDTH // 2, 100)

            # Draw dice
            for i, value in enumerate(dice):
                draw_dice(value, 100 + i * 150, 150)

            # Draw button
            if game.round_count == 0 and dice == [1, 1, 1]:
                button_text = "Start Game"
            elif game.round_count < game.max_rounds - 1:
                button_text = "Roll Dice"
            else:
                button_text = "Finish Game"
            roll_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(window, BLACK, roll_button)
            draw_text(button_text, font, WHITE, roll_button.centerx, roll_button.centery)

            draw_text(message, font, BLACK, WINDOW_WIDTH // 2, 500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if roll_button.collidepoint(event.pos):
                        dice, round_score, game_finished = game.play_round()
                        # Reroll any dice that show 6
                        while 6 in dice:
                            dice = [random.randint(1, 6) if die == 6 else die for die in dice]
                        if game.total_score == 421:
                            message = "You rolled 421 and won the game!"
                            game.game_finished = True
                        else:
                            message = f"Round score: {round_score}"
                            if game_finished:
                                message = f"Game Over! Final Score: {game.total_score}."

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
