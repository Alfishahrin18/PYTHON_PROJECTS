import pygame
import sys
import random

#NEON THEME COLORS 
BLACK = (5, 5, 20)
WHITE = (255, 255, 255)

SNAKE_HEAD = (0, 255, 180)
SNAKE_BODY = (0, 200, 140)
SNAKE_OUTLINE = (0, 120, 80)

FOOD_RED = (255, 30, 120)
FOOD_HIGHLIGHT = (255, 80, 170)

GRID_COLOR = (25, 25, 40)

MENU_TITLE = (0, 255, 200)
MENU_OPTION = (255, 100, 220)
MENU_HIGHLIGHT = (0, 200, 255)

#SETTINGS
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

SPEEDS = {
    'slow': 7,
    'medium': 12,
    'fast': 18
}
# DIFFICULTY MENU 
def difficulty_menu(screen, font):
    while True:
        screen.fill(BLACK)

        title = font.render("SELECT DIFFICULTY", True, MENU_TITLE)
        slow = font.render("1 - SLOW", True, MENU_OPTION)
        medium = font.render("2 - MEDIUM", True, MENU_OPTION)
        fast = font.render("3 - FAST", True, MENU_OPTION)

        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 180))
        screen.blit(slow, (WINDOW_WIDTH // 2 - slow.get_width() // 2, 260))
        screen.blit(medium, (WINDOW_WIDTH // 2 - medium.get_width() // 2, 310))
        screen.blit(fast, (WINDOW_WIDTH // 2 - fast.get_width() // 2, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "slow"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "fast"
# RANDOM FOOD GENERATOR 
def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos
#MAIN GAME LOOP
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake - NEON Edition")

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    # Difficulty selection
    difficulty = difficulty_menu(screen, font)
    speed = SPEEDS[difficulty]

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = random_food_position(snake)

    while True:
        # --- INPUT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)

        # --- MOVE SNAKE ---
        head_x, head_y = snake[0]
        new_head = ((head_x + direction[0]) % GRID_WIDTH,
                    (head_y + direction[1]) % GRID_HEIGHT)

        if new_head in snake:
            pygame.quit()
            sys.exit()

        snake.insert(0, new_head)

        if new_head == food:
            food = random_food_position(snake)
        else:
            snake.pop()

        # --- DRAW EVERYTHING ---
        screen.fill(BLACK)

        # grid
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

        # food
        fx, fy = food
        pygame.draw.rect(screen, FOOD_RED, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, FOOD_HIGHLIGHT,
                         (fx * CELL_SIZE + 4, fy * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        # snake
        for i, (x, y) in enumerate(snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, SNAKE_OUTLINE,
                             (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

        #SCOREBOARD (NEON) 
        score_value = len(snake) - 1
        score_text = font.render(f"Score: {score_value}", True, MENU_HIGHLIGHT)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
