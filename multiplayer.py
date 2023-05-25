import pygame
import time
import random

pygame.init()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)


WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

snake_block = 10
snake_speed = 30

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

clock = pygame.time.Clock()

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

    def draw_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(win, self.color, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH // 2, HEIGHT // 2])

# Game loop
def gameLoop():
    game_over = False

    snake1 = Snake(WIDTH // 4, HEIGHT // 2, YELLOW)
    snake2 = Snake(WIDTH * 3 // 4, HEIGHT // 2, PURPLE)

    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake2.y_change = -snake_block
                    snake2.x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake2.y_change = snake_block
                    snake2.x_change = 0
                elif event.key == pygame.K_LEFT:
                    snake2.x_change = -snake_block
                    snake2.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake2.x_change = snake_block
                    snake2.y_change = 0
                elif event.key == pygame.K_w:
                    snake1.y_change = -snake_block
                    snake1.x_change = 0
                elif event.key == pygame.K_s:
                    snake1.y_change = snake_block
                    snake1.x_change = 0
                elif event.key == pygame.K_a:
                    snake1.x_change = -snake_block
                    snake1.y_change = 0
                elif event.key == pygame.K_d:
                    snake1.x_change = snake_block
                    snake1.y_change = 0

        # Snake boundaries
        if snake1.x >= WIDTH or snake1.x < 0 or snake1.y >= HEIGHT or snake1.y < 0 or \
                snake2.x >= WIDTH or snake2.x < 0 or snake2.y >= HEIGHT or snake2.y < 0:
            game_over = True

        snake1.x += snake1.x_change
        snake1.y += snake1.y_change
        snake2.x += snake2.x_change
        snake2.y += snake2.y_change

        win.fill(BLACK)
        pygame.draw.rect(win, GREEN, [foodx, foody, snake_block, snake_block])

        snake1.snake_list.append([snake1.x, snake1.y])
        snake2.snake_list.append([snake2.x, snake2.y])

        if len(snake1.snake_list) > snake1.snake_length:
            del snake1.snake_list[0]
        if len(snake2.snake_list) > snake2.snake_length:
            del snake2.snake_list[0]

        for pos in snake1.snake_list[:-1]:
            if pos == [snake1.x, snake1.y] or pos == [snake2.x, snake2.y]:
                game_over = True
        for pos in snake2.snake_list[:-1]:
            if pos == [snake2.x, snake2.y] or pos == [snake1.x, snake1.y]:
                game_over = True

        snake1.draw_snake()
        snake2.draw_snake()

        pygame.display.update()

        if snake1.x == foodx and snake1.y == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            snake1.snake_length += 1

        if snake2.x == foodx and snake2.y == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            snake2.snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
