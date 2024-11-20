import pygame
import random
import sys

# Pygame initialisieren
pygame.init()

# Fullscreen-Modus und Farben
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
background_color = (0, 0, 20)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Schriftarten und Taktung
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Spieler-Konfiguration
player_size = 60  # Angepasst für Bildgröße
player_x = screen_width // 2
player_y = screen_height - player_size - 10
player_speed = 5
player_lives = 3
player_ammo = 10

# Gegner-Konfiguration
enemy_width, enemy_height = 50, 50  # Angepasst für Bildgröße
enemy_speed = 1
enemies = []

# Schuss-Konfiguration
bullet_width, bullet_height = 15, 30  # Angepasst für Bildgröße
bullet_speed = 7
bullets = []
ammo_items = []

# Bildpfade
player_image_path = "player_icon.png"
enemy_image_path = "enemy_icon.png"
bullet_image_path = "bullet_icon.png"
ammo_image_path = "ammo_icon.png"

# Laden der Bilder
try:
    player_image = pygame.image.load(player_image_path).convert_alpha()
    enemy_image = pygame.image.load(enemy_image_path).convert_alpha()
    bullet_image = pygame.image.load(bullet_image_path).convert_alpha()
    ammo_image = pygame.image.load(ammo_image_path).convert_alpha()
except pygame.error as e:
    print(f"Fehler beim Laden der Bilder: {e}")
    pygame.quit()
    sys.exit()

# Skalieren der Bilder
player_icon = pygame.transform.scale(player_image, (player_size, player_size))
enemy_icon = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
bullet_icon = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
ammo_icon = pygame.transform.scale(ammo_image, (30, 30))  # Munition-Item-Größe

# Sound initialisieren
try:
    shot_sound = pygame.mixer.Sound("retro_schuss.mp3")
except pygame.error as e:
    print(f"Fehler beim Laden des Schusssounds: {e}")
    shot_sound = None  # Fortfahren ohne Sound

# Hintergrundmusik laden und starten
try:
    pygame.mixer.music.load("sandstorm.mp3")
    pygame.mixer.music.set_volume(0.5)  # Lautstärke anpassen (Wert zwischen 0.0 und 1.0)
    pygame.mixer.music.play(-1)  # Musik in einer Endlosschleife abspielen
except pygame.error as e:
    print(f"Fehler beim Laden der Hintergrundmusik: {e}")

# Spielvariablen
score = 0
level = 1
initial_enemy_count = 20  # Start mit der Gegneranzahl wie Level 8
enemy_spawn_rate = 200
ammo_spawn_rate = 100

# Funktionen für Spieler, Gegner und Schüsse
def draw_player():
    screen.blit(player_icon, (player_x - player_size // 2, player_y - player_size // 2))

def create_enemy():
    if len(enemies) < initial_enemy_count + (level * 2):  # Gegneranzahl basierend auf Level
        x = random.randint(0, screen_width - enemy_width)
        y = random.randint(-100, -40)
        enemy_rect = pygame.Rect(x, y, enemy_width, enemy_height)
        enemies.append(enemy_rect)

def move_enemies():
    global player_lives
    player_rect = pygame.Rect(player_x - player_size // 2, player_y - player_size // 2, player_size, player_size)
    for enemy in enemies[:]:
        enemy.y += enemy_speed + (level * 0.3)
        if enemy.colliderect(player_rect):  # Kollisionsprüfung mit dem Spieler
            player_lives -= 1
            enemies.remove(enemy)
            create_enemy()
        elif enemy.y > screen_height:
            enemies.remove(enemy)
            create_enemy()

def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_icon, (enemy.x, enemy.y))

def shoot():
    global player_ammo
    if player_ammo > 0:
        bullet_rect = pygame.Rect(player_x - bullet_width // 2, player_y - bullet_height, bullet_width, bullet_height)
        bullets.append(bullet_rect)
        if shot_sound:
            shot_sound.play()  # Spiele den Schusssound ab
        player_ammo -= 1  # Ammo hier reduzieren
        return True
    return False

def move_bullets():
    global score
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < -bullet_height:
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):  # Kollisionsprüfung mit Gegnern
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    create_enemy()
                    break

def draw_bullets():
    for bullet in bullets:
        screen.blit(bullet_icon, (bullet.x, bullet.y))

def spawn_ammo():
    x = random.randint(0, screen_width - 30)
    ammo_items.append([x, -30])

def move_ammo():
    global player_ammo
    player_rect = pygame.Rect(player_x - player_size // 2, player_y - player_size // 2, player_size, player_size)
    for item in ammo_items[:]:
        item[1] += 2
        ammo_rect = pygame.Rect(item[0], item[1], 30, 30)
        if ammo_rect.colliderect(player_rect):  # Kollisionsprüfung mit dem Spieler
            player_ammo += 5
            ammo_items.remove(item)
        elif item[1] > screen_height:
            ammo_items.remove(item)

def draw_ammo():
    for item in ammo_items:
        screen.blit(ammo_icon, (item[0], item[1]))

def draw_ui():
    score_text = font.render(f"Score: {score}", True, white)
    lives_text = font.render(f"Lives: {player_lives}", True, white)
    ammo_text = font.render(f"Ammo: {player_ammo}", True, white)
    level_text = font.render(f"Level: {level}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(ammo_text, (10, 70))
    screen.blit(level_text, (10, 100))

def game_over():
    pygame.mixer.music.pause()  # Musik pausieren
    
    selected_option = 0  # 0 für "Retry", 1 für "Exit"
    options = ["Retry", "Exit"]
    while True:
        screen.fill(background_color)
        
        # "Game Over"-Text
        over_text = font.render("Game Over", True, red)
        screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, screen_height // 2 - 150))

        # Aktueller Score und Level anzeigen
        score_text = font.render(f"Score: {score}", True, white)
        level_text = font.render(f"Level: {level}", True, white)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, screen_height // 2 - 60))
        
        # Optionen anzeigen (Retry/Exit)
        for i, option in enumerate(options):
            color = white if i == selected_option else (150, 150, 150)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, screen_height // 2 + i * 50))
        
        # Bildschirm aktualisieren
        pygame.display.flip()

        # Eingaben verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # "Retry"
                        pygame.mixer.music.stop()  # Musik stoppen
                        pygame.mixer.music.play(-1)  # Musik von vorne starten
                        return True
                    elif selected_option == 1:  # "Exit"
                        pygame.quit()
                        sys.exit()

# Hauptspiel-Schleife
for _ in range(initial_enemy_count):  # Anfangsanzahl der Gegner
    create_enemy()

ammo_timer, enemy_timer = 0, 0

while True:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot()
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    # Spielersteuerung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_size // 2:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size // 2:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > player_size // 2:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_size // 2:
        player_y += player_speed

    # Gegner und Munition spawnen
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_rate // max(level, 1):
        create_enemy()
        enemy_timer = 0

    ammo_timer += 1
    if ammo_timer >= ammo_spawn_rate:
        spawn_ammo()
        ammo_timer = 0

    # Elemente im Spiel bewegen
    move_enemies()
    move_bullets()
    move_ammo()

    # Zeichnen
    draw_player()
    draw_enemies()
    draw_bullets()
    draw_ammo()
    draw_ui()

    # Schwierigkeitsgrad erhöhen
    if score > level * 100:
        level += 1

    # Spielende
    if player_lives <= 0:
        if game_over():
            # Reset des Spiels
            player_lives, player_ammo, score, level = 3, 10, 0, 1
            enemies.clear()
            bullets.clear()
            ammo_items.clear()
            for _ in range(initial_enemy_count):
                create_enemy()

    # Bildschirm aktualisieren
    pygame.display.flip()
    clock.tick(60)
