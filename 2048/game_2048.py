import pygame
import random
import sys
from pygame import gfxdraw
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 4
CELL_PADDING = 10
CELL_SIZE = (WINDOW_SIZE - (GRID_SIZE + 1) * CELL_PADDING) // GRID_SIZE
ANIMATION_SPEED = 15

# Colors
BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
SCORE_COLOR = (238, 228, 218)
TEXT_COLOR = (119, 110, 101)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("2048")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 65)
        self.score_font = pygame.font.Font(None, 40)
        self.tile_font = pygame.font.Font(None, 50)
        
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.animations = []
        self.add_new_tile()
        self.add_new_tile()

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            self.animations.append({
                'type': 'spawn',
                'pos': (i, j),
                'value': self.grid[i][j],
                'progress': 0
            })

    def draw_rounded_rect(self, surface, color, rect, radius):
        x, y, width, height = rect
        
        # Draw the main rectangle
        pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
        pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))
        
        # Draw the corners
        for corner_x, corner_y in [(x + radius, y + radius),
                                 (x + width - radius, y + radius),
                                 (x + radius, y + height - radius),
                                 (x + width - radius, y + height - radius)]:
            gfxdraw.aacircle(surface, corner_x, corner_y, radius, color)
            gfxdraw.filled_circle(surface, corner_x, corner_y, radius, color)

    def draw_tile(self, x, y, value, size_factor=1.0, alpha=255):
        if value == 0:
            return

        cell_size = int(CELL_SIZE * size_factor)
        padding = (CELL_SIZE - cell_size) // 2
        
        # Create a surface for the tile
        tile_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        
        # Get color based on value
        color = TILE_COLORS.get(value, TILE_COLORS[2048])
        
        # Draw rounded rectangle
        self.draw_rounded_rect(tile_surface, (*color, alpha), (0, 0, cell_size, cell_size), 10)
        
        # Draw number
        text_color = (119, 110, 101) if value <= 4 else (255, 255, 255)
        text = self.tile_font.render(str(value), True, (*text_color, alpha))
        text_rect = text.get_rect(center=(cell_size // 2, cell_size // 2))
        tile_surface.blit(text, text_rect)
        
        # Draw tile on screen
        self.screen.blit(tile_surface, (x + padding, y + padding))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title and scores
        title = self.title_font.render("2048", True, TEXT_COLOR)
        self.screen.blit(title, (20, 20))
        
        score_text = self.score_font.render(f"Score: {self.score}", True, TEXT_COLOR)
        high_score_text = self.score_font.render(f"Best: {self.high_score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (WINDOW_SIZE - 200, 20))
        self.screen.blit(high_score_text, (WINDOW_SIZE - 200, 50))
        
        # Draw game board
        board_rect = (CELL_PADDING, 100, WINDOW_SIZE - 2 * CELL_PADDING, WINDOW_SIZE - 2 * CELL_PADDING)
        self.draw_rounded_rect(self.screen, GRID_COLOR, board_rect, 10)
        
        # Draw cells and handle animations
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = CELL_PADDING + j * (CELL_SIZE + CELL_PADDING)
                y = 100 + CELL_PADDING + i * (CELL_SIZE + CELL_PADDING)
                
                # Draw empty cell background
                self.draw_rounded_rect(self.screen, TILE_COLORS[0], 
                                     (x, y, CELL_SIZE, CELL_SIZE), 5)
                
                # Draw tile
                if self.grid[i][j] != 0:
                    self.draw_tile(x, y, self.grid[i][j])
        
        # Handle animations
        new_animations = []
        for anim in self.animations:
            if anim['type'] == 'spawn':
                progress = anim['progress'] / 10
                size_factor = 0.1 + 0.9 * progress
                alpha = int(255 * progress)
                
                x = CELL_PADDING + anim['pos'][1] * (CELL_SIZE + CELL_PADDING)
                y = 100 + CELL_PADDING + anim['pos'][0] * (CELL_SIZE + CELL_PADDING)
                
                self.draw_tile(x, y, anim['value'], size_factor, alpha)
                
                anim['progress'] += 1
                if anim['progress'] <= 10:
                    new_animations.append(anim)
        
        self.animations = new_animations
        
        if self.game_over:
            # Draw game over overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE + 100), pygame.SRCALPHA)
            overlay.fill((238, 228, 218, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.title_font.render("Game Over!", True, TEXT_COLOR)
            restart_text = self.score_font.render("Press R to Restart", True, TEXT_COLOR)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)

    def move(self, direction):
        if self.game_over:
            return False

        moved = False
        if direction in ['UP', 'DOWN']:
            for j in range(GRID_SIZE):
                column = [self.grid[i][j] for i in range(GRID_SIZE)]
                if direction == 'UP':
                    new_column = self.merge(column)
                else:
                    new_column = self.merge(column[::-1])[::-1]
                
                if new_column != column:
                    moved = True
                    for i in range(GRID_SIZE):
                        self.grid[i][j] = new_column[i]
        
        else:  # LEFT or RIGHT
            for i in range(GRID_SIZE):
                row = self.grid[i][:]
                if direction == 'LEFT':
                    new_row = self.merge(row)
                else:
                    new_row = self.merge(row[::-1])[::-1]
                
                if new_row != row:
                    moved = True
                    self.grid[i] = new_row

        if moved:
            self.add_new_tile()
            if self.is_game_over():
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
        
        return moved

    def merge(self, line):
        # Remove zeros and merge identical tiles
        new_line = [x for x in line if x != 0]
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i + 1]:
                new_line[i] *= 2
                self.score += new_line[i]
                new_line.pop(i + 1)
                new_line.append(0)
        
        # Pad with zeros
        new_line.extend([0] * (GRID_SIZE - len(new_line)))
        return new_line

    def is_game_over(self):
        # Check for empty cells
        if any(0 in row for row in self.grid):
            return False
        
        # Check for possible merges
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j + 1] or \
                   self.grid[j][i] == self.grid[j + 1][i]:
                    return False
        return True

def main():
    game = Game2048()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.reset_game()
                elif not game.game_over:
                    if event.key == pygame.K_UP:
                        game.move('UP')
                    elif event.key == pygame.K_DOWN:
                        game.move('DOWN')
                    elif event.key == pygame.K_LEFT:
                        game.move('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        game.move('RIGHT')

        game.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()