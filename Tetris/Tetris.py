import pygame
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
CELL_SIZE = 30

GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

SHAPES = [
    [[1, 1, 1, 1]],  # I-фигура
    [[1, 1, 1], [1]],  # L-фигура
    [[1, 1, 1], [0, 0, 1]],  # J-фигура
    [[1, 1], [1, 1]],  # O-фигура
    [[1, 1, 1], [0, 1, 0]],  # T-фигура
    [[1, 1, 0], [0, 1, 1]],  # S-фигура
    [[0, 1, 1], [1, 1]]  # Z-фигура
]

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice([CYAN, BLUE, ORANGE, YELLOW, GREEN, RED])
        piece = {'shape': shape, 'color': color, 'x': GRID_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}
        return piece

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_piece(self, piece):
        shape = piece['shape']
        color = piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, (piece['x'] * CELL_SIZE + x * CELL_SIZE,
                                                         piece['y'] * CELL_SIZE + y * CELL_SIZE,
                                                         CELL_SIZE, CELL_SIZE))

    def move_piece(self, dx, dy):
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
        else:
            self.merge_piece()
            self.current_piece = self.new_piece()
            if self.check_collision(self.current_piece, 0, 0):
                self.reset_game()

    def rotate_piece(self):
        rotated_piece = {'shape': list(zip(*reversed(self.current_piece['shape']))),
                         'color': self.current_piece['color'],
                         'x': self.current_piece['x'],
                         'y': self.current_piece['y']}
        if not self.check_collision(rotated_piece, 0, 0):
            self.current_piece = rotated_piece

    def check_collision(self, piece, dx, dy):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT) or self.grid[new_y][new_x]:
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def reset_game(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            self.move_piece(0, 1)

            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)

            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, cell, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            pygame.display.flip()
            self.clock.tick(5)

if __name__ == "__main__":
    game = TetrisGame()
    game.run_game()
