import pygame
import random
import math

# Initializer pygame
pygame.init()

# Sett opp skjermen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(" enemies skyte spill")

# Definer fargene
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Last inn bilder som skal bli brukt 
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (40, 40))
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 60))
grass_image = pygame.image.load("grass.png")
grass_image = pygame.transform.scale(grass_image, (200, 200))
powerup_image = pygame.image.load("powerup.png")
powerup_image = pygame.transform.scale(powerup_image, (30, 30))

# Definer spiller 
player_size = 40
player_pos = [screen_width // 2, screen_height // 2]
player_speed = 3

# Definer camera 
camera_pos = [0, 0]

# Definer enemy
num_enemies = 12
enemy_size = 40
enemy_list = []
for _ in range(num_enemies):
    enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
    enemy_list.append(enemy_pos)

# Definer skudd 
projectile_size = 5
projectile_list = []

# Definer power-ups
powerup_size = 30
powerup_list = []
powerup_spawn_delay = 5000  # millisekunder
last_powerup_spawn = pygame.time.get_ticks()

    




# Definer spill variables
score = 0
game_active = True
clock = pygame.time.Clock()

# Funksjoner for kamera bevegelse 
def move_camera(target):
    camera_pos[0] += (target[0] - screen_width // 2 - camera_pos[0]) // 20
    camera_pos[1] += (target[1] - screen_height // 2 - camera_pos[1]) // 20

def apply_camera(pos):
    return [pos[0] - camera_pos[0], pos[1] - camera_pos[1]]

# Funksjon for å spawne powerups
def spawn_powerup():
    powerup_pos = [random.randint(0, screen_width - powerup_size), random.randint(0, screen_height - powerup_size)]
    powerup_list.append(powerup_pos)

# Funksjon for at spillet skal være over skjermen 
def show_game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text, text_rect)

    score_text = font.render("Score: " + str(score), True, GREEN)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.flip()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                # skyt skudd der musen klikker 
                mouse_pos = pygame.mouse.get_pos()
                angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
                projectile_pos = list(player_pos)
                projectile_vel = [math.cos(angle) * 5, math.sin(angle) * 5]
                projectile_list.append((projectile_pos, projectile_vel))

            else:
                # Reset spillet når du klikker med musen på game over skjermen
                game_active = True
                player_pos = [screen_width // 2, screen_height // 2]
                enemy_list.clear()
                for _ in range(num_enemies):
                    enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
                    enemy_list.append(enemy_pos)
                projectile_list.clear()
                powerup_list.clear()
                score = 0

    if game_active:
        # oppdater spiller 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # oppdater enemy 
        for enemy_idx, enemy_pos in enumerate(enemy_list):
            enemy_vel = [random.randint(-2, 2), random.randint(-2, 2)]
            enemy_pos[0] += enemy_vel[0]
            enemy_pos[1] += enemy_vel[1]

            # sjekk om enemy treffer spilleren 
            if (
                enemy_pos[0] >= player_pos[0] - enemy_size
                and enemy_pos[0] < player_pos[0] + player_size
                and enemy_pos[1] >= player_pos[1] - enemy_size
                and enemy_pos[1] < player_pos[1] + player_size
            ):
                game_active = False

        # Updater skudd position 
        for projectile in projectile_list:
            projectile[0][0] += projectile[1][0]
            projectile[0][1] += projectile[1][1]

            # fjern skudd som går vekk fra kameraet 
            if (
                projectile[0][0] < 0
                or projectile[0][0] >= screen_width
                or projectile[0][1] < 0
                or projectile[0][1] >= screen_height
            ):
                projectile_list.remove(projectile)

            # sjekk for kolisjon med enemy
            for enemy_pos in enemy_list:
                if (
                    projectile[0][0] >= enemy_pos[0] - enemy_size
                    and projectile[0][0] < enemy_pos[0] + enemy_size
                    and projectile[0][1] >= enemy_pos[1] - enemy_size
                    and projectile[0][1] < enemy_pos[1] + enemy_size
                ):
                    enemy_list.remove(enemy_pos)
                    projectile_list.remove(projectile)
                    score += 1

        # oppdater kamera position
        move_camera(player_pos)

        # Spawn power ups 
        current_time = pygame.time.get_ticks()
        if current_time - last_powerup_spawn >= powerup_spawn_delay:
            spawn_powerup()
            last_powerup_spawn = current_time

        # last inn spillet 
        screen.fill(WHITE)

        # tegn gresset 
        for x in range(screen_width // 80 + 1):
            for y in range(screen_height // 80 + 1):
                screen.blit(grass_image, (x * 80 - camera_pos[0], y * 80 - camera_pos[1]))

        # tegn enemies
        for enemy_pos in enemy_list:
            enemy_pos_camera = apply_camera(enemy_pos)
            screen.blit(enemy_image, (enemy_pos_camera[0], enemy_pos_camera[1]))

        # tegn skudd
        for projectile in projectile_list:
            projectile_pos_camera = apply_camera(projectile[0])
            pygame.draw.circle(screen, RED, (projectile_pos_camera[0], projectile_pos_camera[1]), projectile_size)

        # tegn power-ups
        for powerup_pos in powerup_list:
            powerup_pos_camera = apply_camera(powerup_pos)
            screen.blit(powerup_image, (powerup_pos_camera[0], powerup_pos_camera[1]))

        # tegn spilleren  
        player_pos_camera = apply_camera(player_pos)
        screen.blit(player_image, (player_pos_camera[0], player_pos_camera[1]))

        # tegn score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, GREEN)
        screen.blit(score_text, (10, 10))

        # oppdater  displayet 
        pygame.display.update()

    else:
        show_game_over_screen()

    # Set frame raten 
    clock.tick(60)
