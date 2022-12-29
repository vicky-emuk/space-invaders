import pygame

# Initalise game
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 32)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

background_image = pygame.image.load('background.jpg')
player_image = pygame.image.load('player.png')
enemy_image = pygame.image.load('enemy.png')
bullet_image = pygame.image.load('bullet.png')

player_x = 370
player_y = 480
player_dx = 0
player_x = 370
player_y = 480

bullet_x = 0
bullet_y = SCREEN_HEIGHT + 10
bullet_dy = 6
bullet_state = "ready"

enemy_dy = 40
enemy_list = []

level = 0
score = 0

game_over = False
game_over_text = font.render("Game Over", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

running = True

# Functions
def draw_enemy(x, y):
    if x is not None and y is not None:
        screen.blit(enemy_image, (x, y))

def player(x, y):
    screen.blit(player_image, (x, y))

def fire_bullet(x, y):
    screen.blit(bullet_image, (x + 16, y + 10))
    pygame.display.update()
    
def is_collision(enemy_x, enemy_y, player_x, player_y):
    if enemy_x is None or enemy_y is None:
        return False
    distance = ((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2) ** 0.5
    if distance < 27:
        return True
    else:
        return False
    
# Game loop
while running:
    # Check if all enemies are dead
    enemies_left = False
    for enemy_row in enemy_list:
        for enemy in enemy_row:
            if enemy[0] is not None and enemy[1] is not None:
                enemies_left = True
                break
        if enemies_left:
            break
    # If all enemies are gone, increase level and reset enemy rows
    if not enemies_left:
        level += 1
        enemy_list = []
        for i in range(level):
            enemy_row = []
            for j in range(10):
                enemy_x = 50 + j * 50
                enemy_y = 50 + i * 50
                enemy_dx = 1
                enemy_row.append([enemy_x, enemy_y, enemy_dx])
            enemy_list.append(enemy_row)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Handle keystrokes
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_dx = -3
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_dx = 3
            if event.key == pygame.K_SPACE:
                bullet_x = player_x
                bullet_y = player_y - 25
                bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_dx = 0
                
        # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_dy
        if bullet_y <= 0:
            bullet_y = SCREEN_HEIGHT + 10
            bullet_state = "ready"
        # Check if bullet has hit an enemy
        # Check for collisions
        for i in range(len(enemy_list)):
            for j in range(len(enemy_list[i])):
                if enemy_list[i][j] is not None:
                    enemy_x, enemy_y, enemy_dx = enemy_list[i][j]
                    if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
                        bullet_y = SCREEN_HEIGHT + 10
                        bullet_state = "ready"
                        enemy_list[i][j] = None
                        score += 1
    
    # Player movement bounds
    player_x += player_dx
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    
    # Enemy movement
    for i in range(len(enemy_list)):
        for j in range(len(enemy_list[i])):
            if enemy_list[i][j] is not None:
                enemy_x, enemy_y, enemy_dx = enemy_list[i][j]
                enemy_x += enemy_dx
                if enemy_x <= 0 or enemy_x >= 736:
                    enemy_dx =- enemy_dx  # Reverse the direction of movement
                    enemy_y += enemy_dy  # Drop down a row
                enemy_list[i][j] = [enemy_x, enemy_y, enemy_dx]
            
        enemy_list = [row for row in enemy_list if row]
        enemy_list = [[enemy for enemy in row if enemy] for row in enemy_list]
            
        if enemy_y >= player_y:
                game_over = True
                break
        if game_over:
            break
        
    # Remove empty rows and None elements from enemy_list
    for i in range(len(enemy_list)):
        enemy_row = enemy_list[i]
        if enemy_row is None:
            enemy_list.remove(enemy_row)
        else:
            for j in range(len(enemy_row)):
                enemy = enemy_row[j]
                if enemy is None:
                    enemy_row.remove(enemy)

            
    
    # Clear the screen
    screen.blit(background_image, (0, 0))
    
    # Draw the player and enemy ships
    player(player_x, player_y)
    for i in enemy_list:
        for j in i:
            enemy_x, enemy_y, enemy_dx = j
            draw_enemy(enemy_x, enemy_y)
    
    # Display the score + level
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (160, 10))
    
    # Display the game over screen if the game is over
    if game_over:
        screen.blit(game_over_text, game_over_rect)
    
    # Update the display
    pygame.display.update()
