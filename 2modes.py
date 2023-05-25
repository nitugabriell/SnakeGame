import pygame
import pygame_gui
import time
import random

pygame.init()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))

snake_block = 10
snake_speed = 30

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

clock = pygame.time.Clock()

# Setting up pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

play_button_classic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH//2 - 50, HEIGHT//2 - 50), (100, 50)), text='Classic', manager=manager)
play_button_limited_moves = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH//2 - 50, HEIGHT//2 + 50), (100, 50)), text='Limited Moves', manager=manager)

# Snake classes
class Snake:
    def __init__(self, x, y, color):
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.snake_length = 1
        self.x = x
        self.y = y
        self.color = color
        self.invulnerable = False
        self.start_time = None
        self.moves = 0

    def draw_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(win, self.color, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH // 2, HEIGHT // 2])

# Let's add some walls
walls = [[100, 200, 400, 10], [200, 300, 10, 200]]

# Generate food for limited moves mode
def generate_food_limited(food_number):
    foods = []
    for _ in range(food_number):
        foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
        foods.append([foodx, foody])
    return foods

# Draw food for limited moves mode
def draw_food_limited(foods):
    for food in foods:
        pygame.draw.rect(win, GREEN, [food[0], food[1], snake_block, snake_block])

# Game loop
def gameLoop(mode='classic'):
    game_over = False

    snake1 = Snake(WIDTH // 4, HEIGHT // 2, YELLOW)

    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    # Limited moves mode
    if mode == 'limited_moves':
        snake1.moves = 100  # Number of moves the snake can make
        foods = generate_food_limited(20)  # Generate 20 food items

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake1.y_change = -snake_block
                    snake1.x_change = 0
                    if mode == 'limited_moves':
                        snake1.moves -= 1
                elif event.key == pygame.K_DOWN:
                    snake1.y_change = snake_block
                    snake1.x_change = 0
                    if mode == 'limited_moves':
                        snake1.moves -= 1
                elif event.key == pygame.K_LEFT:
                    snake1.x_change = -snake_block
                    snake1.y_change = 0
                    if mode == 'limited_moves':
                        snake1.moves -= 1
                elif event.key == pygame.K_RIGHT:
                    snake1.x_change = snake_block
                    snake1.y_change = 0
                    if mode == 'limited_moves':
                        snake1.moves -= 1

        # Snake boundaries
        if snake1.x >= WIDTH or snake1.x < 0 or snake1.y >= HEIGHT or snake1.y < 0:
            game_over = True

        snake1.x += snake1.x_change
        snake1.y += snake1.y_change

        win.fill(BLACK)

        if mode == 'classic':
            pygame.draw.rect(win, GREEN, [foodx, foody, snake_block, snake_block])
        elif mode == 'limited_moves':
            draw_food_limited(foods)

        snake1.snake_list.append([snake1.x, snake1.y])

        if len(snake1.snake_list) > snake1.snake_length:
            del snake1.snake_list[0]

        for pos in snake1.snake_list[:-1]:
            if pos == [snake1.x, snake1.y]:
                game_over = True

        snake1.draw_snake()

        pygame.display.update()

        # Food consumption
        if mode == 'classic':
            if snake1.x == foodx and snake1.y == foody:
                foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
                snake1.snake_length += 1
        elif mode == 'limited_moves':
            for food in foods:
                if snake1.x == food[0] and snake1.y == food[1]:
                    foods.remove(food)
                    snake1.snake_length += 1
                    break

        if mode == 'limited_moves' and snake1.moves <= 0:
            game_over = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Main menu loop
def mainMenuLoop():
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button_classic:
                        gameLoop('classic')
                    if event.ui_element == play_button_limited_moves:
                        gameLoop('limited_moves')

            manager.process_events(event)

        manager.update(time_delta)
        win.fill(BLACK)
        manager.draw_ui(win)
        pygame.display.update()

mainMenuLoop()
