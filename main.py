import pygame
import sys
import random

# Настройки
W = 800
H = 600
CELL = 20
FPS = 60

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Цвета
BG = (20, 20, 35)
SNAKE_HEAD = (50, 255, 50)
SNAKE_BODY = (40, 200, 40)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Цвета яблок
APPLE_COLORS = [
    (255, 50, 50),    # Красный
    (255, 165, 0),    # Оранжевый
    (255, 255, 0),    # Жёлтый
    (0, 200, 0),      # Зелёный
    (100, 200, 255),  # Голубой
    (200, 100, 255),  # Фиолетовый
]

# Глобальные переменные (рекорд сохраняется!)
high_score = 0
last_direction_change = 0

def reset_game():
    global snake, direction, apple_pos, apple_color, score, speed, game_over
    global next_direction
    
    snake = [(W//2//CELL, H//2//CELL)]
    direction = (1, 0)
    next_direction = (1, 0)
    
    # Первое яблоко
    apple_pos = (random.randint(0, W//CELL-1), random.randint(0, H//CELL-1))
    apple_color = random.choice(APPLE_COLORS)
    
    # Счет обнуляется, но high_score сохраняется!
    score = 0
    speed = 10
    game_over = False
    
    return next_direction

next_direction = reset_game()

# Главный цикл
while True:
    current_time = pygame.time.get_ticks()
    
    # События
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if e.type == pygame.KEYDOWN:
            if game_over:
                if e.key == pygame.K_SPACE:
                    next_direction = reset_game()
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                # Защита от быстрых нажатий
                if current_time - last_direction_change > 100:
                    if e.key == pygame.K_w and direction != (0, 1):
                        next_direction = (0, -1)
                        last_direction_change = current_time
                    elif e.key == pygame.K_s and direction != (0, -1):
                        next_direction = (0, 1)
                        last_direction_change = current_time
                    elif e.key == pygame.K_a and direction != (1, 0):
                        next_direction = (-1, 0)
                        last_direction_change = current_time
                    elif e.key == pygame.K_d and direction != (-1, 0):
                        next_direction = (1, 0)
                        last_direction_change = current_time
                    elif e.key == pygame.K_ESCAPE:
                        game_over = True
    
    # Движение
    if not game_over:
        direction = next_direction
        
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        
        # Проверка столкновений
        if (new_head[0] < 0 or new_head[0] >= W//CELL or 
            new_head[1] < 0 or new_head[1] >= H//CELL or
            new_head in snake):
            game_over = True
        else:
            snake.insert(0, new_head)
            
            # Проверка яблока
            if new_head == apple_pos:
                score += 1
                
                # Обновляем рекорд
                if score > high_score:
                    high_score = score
                
                # Скорость
                if score % 5 == 0 and speed < 30:
                    speed += 1
                
                # Новое яблоко
                free_cells = []
                for x in range(W//CELL):
                    for y in range(H//CELL):
                        if (x, y) not in snake:
                            free_cells.append((x, y))
                
                if free_cells:
                    apple_pos = random.choice(free_cells)
                else:
                    apple_pos = (random.randint(0, W//CELL-1), random.randint(0, H//CELL-1))
                
                apple_color = random.choice(APPLE_COLORS)
            else:
                snake.pop()
    
    # Отрисовка
    screen.fill(BG)
    
    # Яблоко
    pygame.draw.rect(screen, apple_color, 
                    (apple_pos[0]*CELL, apple_pos[1]*CELL, CELL, CELL))
    
    # Змейка
    for i, (x, y) in enumerate(snake):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(screen, color, (x*CELL, y*CELL, CELL, CELL))
    
    # Счет и рекорд (рекорд сохраняется!)
    screen.blit(font.render(f"Счет: {score}", True, GOLD), (10, 10))
    screen.blit(font.render(f"Рекорд: {high_score}", True, GOLD), (W - 150, 10))
    
    # Длина
    screen.blit(font.render(f"Длина: {len(snake)}", True, WHITE), (10, 50))
    
    # Подсказка
    if not game_over:
        screen.blit(font.render("WASD - движение", True, (180, 180, 180)), 
                   (W//2 - 100, H - 40))
    
    # Game Over
    if game_over:
        screen.blit(font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 100)), 
                   (W//2-100, H//2-50))
        screen.blit(font.render(f"Счет: {score}", True, GOLD), 
                   (W//2-60, H//2))
        screen.blit(font.render(f"Рекорд: {high_score}", True, GOLD), 
                   (W//2-70, H//2+40))
        screen.blit(font.render("ПРОБЕЛ - новая игра", True, WHITE), 
                   (W//2-120, H//2+80))
        screen.blit(font.render("ESC - выход", True, WHITE), 
                   (W//2-80, H//2+120))
    
    pygame.display.flip()
    clock.tick(speed if not game_over else FPS)