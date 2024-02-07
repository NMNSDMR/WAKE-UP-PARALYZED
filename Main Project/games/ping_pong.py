import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Цвета
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

# Размеры платформ и надписи
PAD_WIDTH, PAD_HEIGHT = 10, 100
FONT_SIZE = 100

# Скорость платформ и надписи
PAD_SPEED = 5
FONT_SPEED = 2

# Начальные позиции платформ
player1_pos = [PAD_WIDTH, HEIGHT // 2 - PAD_HEIGHT // 2]
player2_pos = [WIDTH - PAD_WIDTH * 2, HEIGHT // 2 - PAD_HEIGHT // 2]

# Начальная позиция надписи
font_pos = [WIDTH // 2 - FONT_SIZE // 3, HEIGHT // 2 - FONT_SIZE // 2]

# Начальная скорость надписи
font_vel = [FONT_SPEED, FONT_SPEED]

# Функция отрисовки платформ и надписи
def draw(canvas):
    canvas.fill(BLACK)
    pygame.draw.rect(canvas, (255, 255, 255), (player1_pos[0], player1_pos[1], PAD_WIDTH, PAD_HEIGHT))
    pygame.draw.rect(canvas, (255, 255, 255), (player2_pos[0], player2_pos[1], PAD_WIDTH, PAD_HEIGHT))
    font_surface = font.render("DVD", True, random.choice(COLORS))
    canvas.blit(font_surface, font_pos)

# Обновление позиций платформ и надписи
def update():
    global font_pos, font_vel

    # Обновление позиции надписи
    font_pos[0] += int(font_vel[0])
    font_pos[1] += int(font_vel[1])

    # Отскок от границ поля
    if font_pos[0] <= 0 or font_pos[0] >= WIDTH - FONT_SIZE:
        font_vel[0] = -font_vel[0]
    if font_pos[1] <= 0 or font_pos[1] >= HEIGHT - FONT_SIZE:
        font_vel[1] = -font_vel[1]

# Основной игровой цикл
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Управление платформами
    if keys[pygame.K_w]:
        player1_pos[1] -= PAD_SPEED
    if keys[pygame.K_s]:
        player1_pos[1] += PAD_SPEED
    if keys[pygame.K_UP]:
        player2_pos[1] -= PAD_SPEED
    if keys[pygame.K_DOWN]:
        player2_pos[1] += PAD_SPEED

    # Ограничения для платформ
    if player1_pos[1] <= 0:
        player1_pos[1] = 0
    elif player1_pos[1] >= HEIGHT - PAD_HEIGHT:
        player1_pos[1] = HEIGHT - PAD_HEIGHT
    if player2_pos[1] <= 0:
        player2_pos[1] = 0
    elif player2_pos[1] >= HEIGHT - PAD_HEIGHT:
        player2_pos[1] = HEIGHT - PAD_HEIGHT

    update()

    draw(WINDOW)
    pygame.display.update()
    clock.tick(60)