import random
import sys
import pygame

# Window settings
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10

# Colors
BLACK = (20, 20, 20)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 50, 50)
WHITE = (245, 245, 245)


def draw_text(surface, text, size, color, center):
    font = pygame.font.SysFont("arial", size, bold=True)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_r:
                    self.reset()

                elif event.key in (pygame.K_UP, pygame.K_w) and self.direction != (0, 1):
                    self.next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != (0, -1):
                    self.next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != (1, 0):
                    self.next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != (-1, 0):
                    self.next_direction = (1, 0)

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Collision with walls
        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over = True
            return

        # Collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 35, 35), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 35, 35), (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

        # Draw food
        fx, fy = self.food
        food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, food_rect, border_radius=4)

        # Draw score
        draw_text(self.screen, f"Score: {self.score}", 24, WHITE, (70, 20))

        if self.game_over:
            draw_text(self.screen, "Game Over", 42, WHITE, (WIDTH // 2, HEIGHT // 2 - 20))
            draw_text(self.screen, "Press R to restart", 24, WHITE, (WIDTH // 2, HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
