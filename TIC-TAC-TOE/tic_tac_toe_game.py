import pygame

# Settings for the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_GREEN = (0, 255, 0)
NEON_PINK = (255, 20, 147)

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 60)

def draw_text(screen, text, color, x, y):
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect(center=(x, y))
    screen.blit(rendered_text, rect)

class TicTacToe:
    def __init__(self):
        self.board = [None] * 9
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_marks()
        self.draw_status()

    def draw_grid(self):
        for x in range(1, 3):
            pygame.draw.line(screen, NEON_BLUE, (x * SCREEN_WIDTH // 3, 0),
                             (x * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 5)
            pygame.draw.line(screen, NEON_BLUE, (0, x * SCREEN_HEIGHT // 3),
                             (SCREEN_WIDTH, x * SCREEN_HEIGHT // 3), 5)

    def draw_marks(self):
        for idx, mark in enumerate(self.board):
            if mark:
                x = (idx % 3) * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 6
                y = (idx // 3) * SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 6
                color = NEON_GREEN if mark == "X" else NEON_PINK
                draw_text(screen, mark, color, x, y)

    def draw_status(self):
        if self.winner:
            status_text = f"Player {self.winner} Wins!"
            status_color = NEON_GREEN
        elif self.is_board_full():
            status_text = "It's a Draw!"
            status_color = NEON_BLUE
        else:
            status_text = f"Player {self.current_player}'s Turn"
            status_color = NEON_PINK

        draw_text(screen, status_text, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    def handle_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        row = y // (SCREEN_HEIGHT // 3)
        col = x // (SCREEN_WIDTH // 3)
        idx = row * 3 + col

        if self.board[idx] is None:
            self.board[idx] = self.current_player
            self.check_winner()
            if not self.winner and not self.is_board_full():
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and self.board[combo[0]] is not None:
                self.winner = self.board[combo[0]]
                self.game_over = True
                return

        if self.is_board_full():
            self.game_over = True

    def is_board_full(self):
        return all(self.board)

    def reset_game(self):
        self.board = [None] * 9
        self.current_player = "X"
        self.winner = None
        self.game_over = False

# Main loop
def main():
    clock = pygame.time.Clock()
    game = TicTacToe()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset_game()

        game.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
