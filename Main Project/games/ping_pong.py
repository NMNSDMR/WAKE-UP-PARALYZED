import pygame
import sys

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Размеры платформ и мяча
PAD_WIDTH, PAD_HEIGHT = 10, 100
BALL_RADIUS = 10

# Скорость платформ и мяча
PAD_SPEED = 5
BALL_X_SPEED = 4
BALL_Y_SPEED = 4

# Начальные позиции платформ
player1_pos = [PAD_WIDTH, HEIGHT // 2 - PAD_HEIGHT // 2]
player2_pos = [WIDTH - PAD_WIDTH * 2, HEIGHT // 2 - PAD_HEIGHT // 2]

# Начальная позиция мяча
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [BALL_X_SPEED, BALL_Y_SPEED]

# Функция отрисовки платформ и мяча
def draw(canvas):
    canvas.fill(BLACK)
    pygame.draw.rect(canvas, WHITE, (player1_pos[0], player1_pos[1], PAD_WIDTH, PAD_HEIGHT))
    pygame.draw.rect(canvas, WHITE, (player2_pos[0], player2_pos[1], PAD_WIDTH, PAD_HEIGHT))
    pygame.draw.circle(canvas, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

# Обновление позиций платформ и мяча
def update():
    global ball_pos, ball_vel, player1_pos, player2_pos

    # Обновление позиции мяча
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    # Отскок от верхней и нижней границ поля
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # Отскок от платформ
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= player1_pos[1] and ball_pos[1] <= player1_pos[1] + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] >= player2_pos[1] and ball_pos[1] <= player2_pos[1] + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]

    # Проверка на выход мяча за границы поля (гол)
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= WIDTH - BALL_RADIUS:
        reset()

# Перезапуск игры после гола
def reset():
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [BALL_X_SPEED, BALL_Y_SPEED]

# Основной игровой цикл
clock = pygame.time.Clock()
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