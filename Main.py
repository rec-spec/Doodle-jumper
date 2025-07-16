import pygame
import random
import sys
import os

pygame.init()

# Fullscreen mode
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = win.get_size()
pygame.display.set_caption("Doodle Run")
clock = pygame.time.Clock()

# Load assets
bg_game = pygame.image.load("assets/background.png").convert()
bg_menu = pygame.image.load("assets/menu_bg.png").convert()
player_img = pygame.image.load("assets/player.png").convert_alpha()
rock_img = pygame.image.load("assets/rock.png").convert_alpha()
coin_img = pygame.image.load("assets/coin.png").convert_alpha()

# Music setup
pygame.mixer.init()
music_on = True
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)

font = pygame.font.SysFont(None, 40)

player = pygame.Rect(100, 300, 50, 50)
gravity = 0
jumping = False
rocks = []
coins = []
score = 0
game_over = False
game_state = "menu"  # "menu", "play", "settings", "credits"

def reset_game():
    global rocks, coins, score, game_over, player, gravity
    player.y = 300
    gravity = 0
    rocks.clear()
    coins.clear()
    score = 0
    game_over = False

def draw_text(text, x, y, center=True, color=(0,0,0)):
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    win.blit(txt, rect)

def draw_menu():
    win.blit(bg_menu, (0, 0))
    draw_text("DOODLE RUN", WIDTH // 2, 60)
    draw_text("1. Play", WIDTH // 2, 140)
    draw_text("2. Settings", WIDTH // 2, 190)
    draw_text("3. Credits", WIDTH // 2, 240)
    draw_text("4. Quit", WIDTH // 2, 290)
    pygame.display.update()

def draw_settings():
    win.fill((220, 220, 220))
    draw_text("SETTINGS", WIDTH // 2, 60)
    draw_text(f"1. Music: {'On' if music_on else 'Off'}", WIDTH // 2, 150)
    draw_text("2. Back", WIDTH // 2, 220)
    pygame.display.update()

def draw_credits():
    win.fill((240, 240, 240))
    draw_text("CREDITS", WIDTH // 2, 60)
    draw_text("Scripter: Elijah", WIDTH // 2, 150)
    draw_text("Tester: Arlo", WIDTH // 2, 200)
    draw_text("Press any key to return", WIDTH // 2, 300)
    pygame.display.update()

def draw_game():
    win.blit(bg_game, (0, 0))
    win.blit(player_img, (player.x, player.y))
    for rock in rocks:
        win.blit(rock_img, (rock.x, rock.y))
    for coin in coins:
        win.blit(coin_img, (coin.x, coin.y))
    draw_text(f"Score: {score}", 10, 10, center=False)
    if game_over:
        draw_text("Game Over! Press R to restart", WIDTH // 2, HEIGHT // 2, (255, 0, 0))
    pygame.display.update()

spawn_timer = 0

running = True
while running:
    clock.tick(60)

    if game_state == "menu":
        draw_menu()
    elif game_state == "settings":
        draw_settings()
    elif game_state == "credits":
        draw_credits()
    elif game_state == "play":
        if not game_over:
            gravity += 1
            player.y += gravity
            if player.y >= 300:
                player.y = 300
                jumping = False

            spawn_timer += 1
            if spawn_timer > 60:
                rocks.append(pygame.Rect(WIDTH, 330, 40, 40))
                if random.choice([True, False]):
                    coins.append(pygame.Rect(WIDTH + 20, 260, 30, 30))
                spawn_timer = 0

            for rock in rocks:
                rock.x -= 5
                if player.colliderect(rock):
                    game_over = True
            for coin in coins[:]:
                coin.x -= 5
                if player.colliderect(coin):
                    score += 1
                    coins.remove(coin)

            rocks = [r for r in rocks if r.x > -50]
            coins = [c for c in coins if c.x > -50]

        draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_1:
                    game_state = "play"
                    reset_game()
                elif event.key == pygame.K_2:
                    game_state = "settings"
                elif event.key == pygame.K_3:
                    game_state = "credits"
                elif event.key == pygame.K_4:
                    running = False

            elif game_state == "settings":
                if event.key == pygame.K_1:
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                elif event.key == pygame.K_2:
                    game_state = "menu"

            elif game_state == "credits":
                game_state = "menu"

            elif game_state == "play":
                if event.key == pygame.K_SPACE and player.y == 300:
                    gravity = -20
                if event.key == pygame.K_r and game_over:
                    reset_game()

pygame.quit()
sys.exit()
