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
AQUA = (0, 255, 255)
ORANGE = (255, 105, 0)


WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
intro_style = pygame.font.SysFont(None, 100)

clock = pygame.time.Clock()

pygame.display.set_caption('Snake.io')

# Setting up pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

play_button_classic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH//2 - 50, HEIGHT//2 - 50), (150, 50)), text='Classic', manager=manager)
play_button_limited_moves = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH//2 - 50, HEIGHT//2 + 50), (150, 50)), text='Limited Moves', manager=manager)
play_button_multiplayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH//2 - 50, HEIGHT//2 + 150), (150, 50)), text='Multiplayer', manager=manager)
play_button_portal = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH//2 - 50, HEIGHT//2 + 250), (150, 50)), text='Portal mode', manager=manager)


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
            pygame.draw.rect(window, self.color, [x[0], x[1], snake_block, snake_block])
            pygame.draw.rect(window, BLUE, [x[0], x[1], snake_block, snake_block], 2)
        head = self.snake_list[-1]
        pygame.draw.circle(window, RED, (head[0] + 5, head[1] + 5), 3)
        pygame.draw.circle(window, RED, (head[0] + 15, head[1] + 5), 3)

def display_score(score, color):
    score_text = font_style.render("Score: " + str(score), True, color)
    window.blit(score_text, [10, 10])

def display_score2(score, color):
    score_text = font_style.render("Score: " + str(score), True, color)
    window.blit(score_text, [840, 10])

def display_moves(moves, color):
    moves_text = font_style.render("Moves: " + str(moves), True, color)
    window.blit(moves_text, [820, 10])

def display_intro(color):
    text = intro_style.render("Welcome to Snake.io ", True, color)
    window.blit(text, [200, 200])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [WIDTH // 2 - 100, HEIGHT // 2 - 200])

# Generate food for limited moves mode
def generate_food_limited(food_number):
    foods = []
    for _ in range(food_number):
        foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block
        foods.append([foodx, foody])
    return foods

# Draw food for limited moves mode
def draw_food_limited(foods):
    for food in foods:
        pygame.draw.rect(window, GREEN, [food[0], food[1], snake_block, snake_block])

# Game loop
def gameLoop(mode):
    game_over = False
    game_quit = False

    snake1 = Snake(WIDTH // 2, HEIGHT // 2, ORANGE)

    foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block

    # Limited moves mode
    if mode == 'limited_moves':
        snake1.moves = 50  # Number of moves the snake can make
        foods = generate_food_limited(200)  # Generate 20 food items
        display_moves(snake1.moves, ORANGE)
        pygame.display.update()

    while not game_quit:
        while game_over:
            window.fill(BLACK)
            game_over_text = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, BLUE)
            window.blit(game_over_text, [WIDTH / 9, HEIGHT // 2])
            display_score(snake1.snake_length - 1, RED)
            pygame.display.update()

            # Check for game quit or play again
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_quit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        mainMenuLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
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

        window.fill(BLACK)

        if mode == 'classic':
            pygame.draw.rect(window, GREEN, [foodx, foody, snake_block, snake_block])
        elif mode == 'limited_moves':
            draw_food_limited(foods)

        snake1.snake_list.append([snake1.x, snake1.y])

        if len(snake1.snake_list) > snake1.snake_length:
            del snake1.snake_list[0]

        for pos in snake1.snake_list[:-1]:
            if pos == [snake1.x, snake1.y]:
                game_over = True

        snake1.draw_snake()
        display_score(snake1.snake_length - 1, RED)
        if mode == 'limited_moves':
            display_moves(snake1.moves, ORANGE)
        pygame.display.update()

        # Food consumption
        if mode == 'classic':
            if snake1.x == foodx and snake1.y == foody:
                foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
                foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block
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

# Multiplayer mode game loop
def gameLoopMultiplayer():
    game_over1 = False
    game_over2 = False
    game_quit = False

    snake1 = Snake(300, HEIGHT // 2, YELLOW)
    snake2 = Snake(600, HEIGHT // 2, PURPLE)

    foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block

    while not game_quit:
        while game_over1:
            window.fill(BLACK)
            win_text = font_style.render("PURPLE WIN !", True, PURPLE)
            window.blit(win_text, [WIDTH / 3, HEIGHT // 3])
            game_over_text = font_style.render("Press Q-Quit or C-Play Again", True, GREEN)
            window.blit(game_over_text, [WIDTH / 4, HEIGHT // 2])
            display_score(snake1.snake_length - 1, YELLOW)
            display_score2(snake2.snake_length - 1, PURPLE)
            pygame.display.update()

            # Check for game quit or play again
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                    game_over1 = False
                    game_over2 = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_quit = True
                        game_over1 = False
                        game_over2 = False
                    if event.key == pygame.K_c:
                        mainMenuLoop()

        while game_over2:
            window.fill(BLACK)
            win_text = font_style.render("YELLOW WIN !", True, YELLOW)
            window.blit(win_text, [WIDTH / 3, HEIGHT // 3])
            game_over_text = font_style.render("Press Q-Quit or C-Play Again", True, GREEN)
            window.blit(game_over_text, [WIDTH / 4, HEIGHT // 2])
            display_score(snake1.snake_length - 1, YELLOW)
            display_score2(snake2.snake_length - 1, PURPLE)
            pygame.display.update()

            # Check for game quit or play again
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                    game_over1 = False
                    game_over2 = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_quit = True
                        game_over1 = False
                        game_over2 = False
                    if event.key == pygame.K_c:
                        mainMenuLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake1.y_change = -snake_block
                    snake1.x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake1.y_change = snake_block
                    snake1.x_change = 0
                elif event.key == pygame.K_LEFT:
                    snake1.x_change = -snake_block
                    snake1.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake1.x_change = snake_block
                    snake1.y_change = 0
                elif event.key == pygame.K_w:
                    snake2.y_change = -snake_block
                    snake2.x_change = 0
                elif event.key == pygame.K_s:
                    snake2.y_change = snake_block
                    snake2.x_change = 0
                elif event.key == pygame.K_a:
                    snake2.x_change = -snake_block
                    snake2.y_change = 0
                elif event.key == pygame.K_d:
                    snake2.x_change = snake_block
                    snake2.y_change = 0

        # Snake boundaries
        if snake1.x >= WIDTH or snake1.x < 0 or snake1.y >= HEIGHT or snake1.y < 0:
            game_over1 = True
        if snake2.x >= WIDTH or snake2.x < 0 or snake2.y >= HEIGHT or snake2.y < 0:
            game_over2 = True

        snake1.x += snake1.x_change
        snake1.y += snake1.y_change
        snake2.x += snake2.x_change
        snake2.y += snake2.y_change

        window.fill(BLACK)

        pygame.draw.rect(window, GREEN, [foodx, foody, snake_block, snake_block])

        # Grow snake
        snake1.snake_list.append([snake1.x, snake1.y])
        snake2.snake_list.append([snake2.x, snake2.y])

        if len(snake1.snake_list) > snake1.snake_length:
            del snake1.snake_list[0]
        if len(snake2.snake_list) > snake2.snake_length:
            del snake2.snake_list[0]

        for pos in snake1.snake_list[:-1]:
            if pos == [snake1.x, snake1.y] or pos == [snake2.x, snake2.y]:
                game_over1 = True
        for pos in snake2.snake_list[:-1]:
            if pos == [snake2.x, snake2.y] or pos == [snake1.x, snake1.y]:
                game_over1 = True

        snake1.draw_snake()
        snake2.draw_snake()
        display_score(snake1.snake_length - 1, YELLOW)
        display_score2(snake2.snake_length - 1, PURPLE)
        pygame.display.update()

        # Food consumption
        if snake1.x == foodx and snake1.y == foody:
            foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block
            snake1.snake_length += 1

        if snake2.x == foodx and snake2.y == foody:
            foodx = round(random.randrange(20, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(20, HEIGHT - snake_block) / snake_block) * snake_block
            snake2.snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()
def gameLoopPortal():
    game_over = False

    snake1 = Snake(WIDTH // 2, HEIGHT // 2, YELLOW)

    foodx1 = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody1 = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
    foodx2 = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody2 = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake1.y_change = -snake_block
                    snake1.x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake1.y_change = snake_block
                    snake1.x_change = 0
                elif event.key == pygame.K_LEFT:
                    snake1.x_change = -snake_block
                    snake1.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake1.x_change = snake_block
                    snake1.y_change = 0

        snake1.x += snake1.x_change
        snake1.y += snake1.y_change

        # Portal effect
        if snake1.x == foodx1 and snake1.y == foody1:
            snake1.x = foodx2
            snake1.y = foody2
            foodx1 = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody1 = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
            foodx2 = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody2 = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
        elif snake1.x == foodx2 and snake1.y == foody2:
            snake1.x = foodx1
            snake1.y = foody1
            foodx1 = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody1 = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
            foodx2 = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody2 = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

        # Snake boundaries
        if snake1.x >= WIDTH or snake1.x < 0 or snake1.y >= HEIGHT or snake1.y < 0:
            game_over = True

        window.fill(BLACK)

        pygame.draw.rect(window, GREEN, [foodx1, foody1, snake_block, snake_block])
        pygame.draw.rect(window, GREEN, [foodx2, foody2, snake_block, snake_block])

        snake1.snake_list.append([snake1.x, snake1.y])

        if len(snake1.snake_list) > snake1.snake_length:
            del snake1.snake_list[0]

        for pos in snake1.snake_list[:-1]:
            if pos == [snake1.x, snake1.y]:
                game_over = True

        snake1.draw_snake()

        pygame.display.update()

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
                    if event.ui_element == play_button_multiplayer:
                        gameLoopMultiplayer()
                    if event.ui_element == play_button_portal:
                        gameLoopPortal()
                    

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        gameLoop('classic')
                    if event.key == pygame.K_2:
                        gameLoop('limited_moves')
                    if event.key == pygame.K_3:
                        gameLoopMultiplayer()
                    if event.key == pygame.K_4:
                        gameLoopPortal()
                  
            manager.process_events(event)

        manager.update(time_delta)
        window.fill(BLACK)
        manager.draw_ui(window)
        display_intro(YELLOW)
        pygame.display.update()

mainMenuLoop()