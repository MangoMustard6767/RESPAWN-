import pygame
import random
import sys


pygame.init()
pygame.mixer.init()  


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")


WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)


PLAYER_IMG = pygame.image.load("player.png")
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (64, 64))
ENEMY_IMG = pygame.image.load("enemy.png")
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (64, 64))
BULLET_IMG = pygame.image.load("bullet.png")
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (20, 40))
AD_IMG = pygame.image.load("ad.png")
AD_IMG = pygame.transform.scale(AD_IMG, (300, 150))


player_x = 370
player_y = 480
player_speed = 30


bullet_x = 0
bullet_y = 480
bullet_speed = 10
bullet_state = "ready"  


enemy_speed = 3
enemies = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemies.append({
        "x": random.randint(0, 736),
        "y": random.randint(50, 150),
        "speed_x": enemy_speed,
        "speed_y": 40
    })


score = 0
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 64)



def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_end_screen(win=True):
    screen.fill(PURPLE)
    if win:
        title_text = game_over_font.render("YOU WIN", True, WHITE)
        subtitle_text = font.render("See you 2026", True, WHITE)
    else:
        title_text = game_over_font.render("GAME OVER", True, WHITE)
        subtitle_text = font.render("We hope to still see you in 2026", True, WHITE)
    

    screen.blit(title_text, (250, 150))
    screen.blit(subtitle_text, (180, 250))
    screen.blit(AD_IMG, (250, 350))
    pygame.display.update()
    pygame.time.wait(4000)
    pygame.quit()
    sys.exit()

def player(x, y):
    screen.blit(PLAYER_IMG, (x, y))

def enemy(x, y):
    screen.blit(ENEMY_IMG, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BULLET_IMG, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < 27


running = True
while running:
    screen.fill(PURPLE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(player_x, SCREEN_WIDTH - 64))

    
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_x = player_x
            fire_bullet(bullet_x, bullet_y)
           

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    
    for enemy_obj in enemies:
        enemy_obj["x"] += enemy_obj["speed_x"]
        if enemy_obj["x"] <= 0 or enemy_obj["x"] >= SCREEN_WIDTH - 64:
            enemy_obj["speed_x"] *= -1
            enemy_obj["y"] += enemy_obj["speed_y"]

        
        if is_collision(enemy_obj["x"], enemy_obj["y"], bullet_x, bullet_y):
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_obj["x"] = random.randint(0, 736)
            enemy_obj["y"] = random.randint(50, 150)
           
        if score >= 20:
            show_end_screen(win=True)
            break

        
        if enemy_obj["y"] > 440:
            show_end_screen(win=False)
            break

        enemy(enemy_obj["x"], enemy_obj["y"])

    player(player_x, player_y)
    show_score()
    pygame.display.update()
