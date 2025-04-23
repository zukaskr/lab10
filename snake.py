import pygame
import sys
from random import randint

# === 1. 初始化 ===
pygame.init()

CELL_SIZE = 20
WIDTH, HEIGHT = 640, 480
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# 颜色定义
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# === 2. 游戏变量 ===
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE,
        randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE)

score = 0
paused = False
running = True

# === 3. 游戏函数 ===
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def move_snake():
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    snake.insert(0, new_head)
    if new_head == food:
        return True
    else:
        snake.pop()
        return False

def check_collision():
    head = snake[0]
    return (
        head in snake[1:] or
        head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT
    )

def show_game_over(username, score):
    font = pygame.font.SysFont(None, 36)
    game_over_text = font.render(f"Game Over! {username} Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    pygame.time.wait(2000)

def show_start_screen():
    font = pygame.font.SysFont(None, 36)
    text = font.render("Enter your name: ", True, WHITE)
    screen.fill(BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
    pygame.display.flip()

    # 获取用户输入的姓名
    name_input = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_input != "":
                    return name_input
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                else:
                    name_input += event.unicode
        # 更新显示的输入内容
        screen.fill(BLACK)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
        name_text = font.render(name_input, True, WHITE)
        screen.blit(name_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

# === 4. 游戏主程序 ===

# 获取玩家姓名
username = show_start_screen()

# 游戏循环
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)
            elif event.key == pygame.K_p:  # 按P键暂停或继续游戏
                paused = not paused
                print("⏸ Paused" if paused else "▶ Resume")

    if not paused:
        if move_snake():
            score += 10
            food = (randint(0, (WIDTH - CELL_SIZE)//CELL_SIZE) * CELL_SIZE,
                    randint(0, (HEIGHT - CELL_SIZE)//CELL_SIZE) * CELL_SIZE)

        if check_collision():
            show_game_over(username, score)
            running = False

    draw_snake()
    draw_food()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
