import pygame
import random

# game set-up
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space_invaders_icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')

# Player
player_image = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_dx = 0

# Enemy
enemy_image = pygame.image.load('enemy.png')
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_dx = 1
enemy_dy = 40


# Bullet
bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_dx = 0
bullet_dy = 10
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y, score, font):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y):
    screen.blit(enemy_image, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)**0.5
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -5
            if event.key == pygame.K_RIGHT:
                player_dx = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0
         # Player movement bounds
    player_x += player_dx
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    
    # Enemy movement
    enemy_x += enemy_dx
    if enemy_x <= 0 or enemy_x >= 736:
        enemy_dx = -enemy_dx  # Reverse the direction of movement
        enemy_y += enemy_dy  # Drop down a row

    
    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_dy
    
    # Collision
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score += 1
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)
    
    # Game Over
    if enemy_y > 440:
        for i in range(3):
            game_over_text()
            pygame.display.update()
            pygame.time.delay(1000)
        running = False
    
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(10, 10, score, font)
    pygame.display.update()

pygame.quit()