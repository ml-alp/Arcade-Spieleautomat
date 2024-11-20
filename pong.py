import pygame
import sys
import random
import math

# Initialisiere pygame
pygame.init()

# Fenstergröße und Framerate
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Optimiertes Pong")
FPS = 60
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 200)

# Paddle- und Ballparameter
PADDLE_WIDTH, PADDLE_HEIGHT = WIDTH // 40, HEIGHT // 6
BALL_SIZE = WIDTH // 40
PADDLE_SPEED = 10
BALL_SPEED = 7
BALL_ACCELERATION = 0.05  # Beschleunigungsfaktor pro Treffer

# Positionen
paddle1_x, paddle1_y = WIDTH // 40, HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_x, paddle2_y = WIDTH - WIDTH // 40 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
ball_dx, ball_dy = 0, 0  # Zufällig initialisiert

# Punktestände
score1, score2 = 0, 0
game_over = False

# Schriftart
font = pygame.font.SysFont(None, WIDTH // 20)

# Sound (nur einmal laden)
pong_sound = pygame.mixer.Sound("pong.mp3")
pong_sound.set_volume(0.1)  # Lautstärke verringern, um die Leistung zu verbessern

# Spiel zurücksetzen
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    angle = random.uniform(-math.pi / 4, math.pi / 4) + (random.choice([0, math.pi]))
    ball_dx = BALL_SPEED * math.cos(angle)
    ball_dy = BALL_SPEED * math.sin(angle)

def draw():
    """Zeichnet das Spielfeld, Paddles, Ball und Punktestand."""
    WIN.fill(BLACK)

    # Paddles und Ball
    pygame.draw.rect(WIN, WHITE, (paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(WIN, WHITE, (paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(WIN, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Punktestand
    score_surface = font.render(f"{score1}:{score2}", True, WHITE)
    WIN.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 20))

def update_ball():
    """Bewegt den Ball und behandelt Kollisionen."""
    global ball_x, ball_y, ball_dx, ball_dy, score1, score2, game_over

    ball_x += ball_dx
    ball_y += ball_dy

    # Wände
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1
        increase_ball_speed()  # Ball wird schneller nach Wandaufprall

    # Paddle-Kollisionen
    if paddle1_x < ball_x < paddle1_x + PADDLE_WIDTH and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT:
        ball_dx = abs(ball_dx)
        pong_sound.play()
        increase_ball_speed()  # Ball wird schneller nach Paddle-Treffer
    elif paddle2_x < ball_x + BALL_SIZE < paddle2_x + PADDLE_WIDTH and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT:
        ball_dx = -abs(ball_dx)
        pong_sound.play()
        increase_ball_speed()  # Ball wird schneller nach Paddle-Treffer

    # Punktevergabe
    if ball_x < 0:
        score2 += 1
        reset_ball()
    elif ball_x > WIDTH:
        score1 += 1
        reset_ball()

    # Spielende nach 5 Punkten
    if score1 >= 5 or score2 >= 5:
        return True  # Spiel ist vorbei
    return False

def increase_ball_speed():
    """Erhöht die Geschwindigkeit des Balls nach jedem Aufprall."""
    global ball_dx, ball_dy
    ball_dx *= (1 + BALL_ACCELERATION)
    ball_dy *= (1 + BALL_ACCELERATION)

def move_paddles():
    """Bewegt die Paddles basierend auf Tasteneingaben."""
    global paddle1_y, paddle2_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_y = max(0, paddle1_y - PADDLE_SPEED)
    if keys[pygame.K_s]:
        paddle1_y = min(HEIGHT - PADDLE_HEIGHT, paddle1_y + PADDLE_SPEED)
    if keys[pygame.K_UP]:
        paddle2_y = max(0, paddle2_y - PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        paddle2_y = min(HEIGHT - PADDLE_HEIGHT, paddle2_y + PADDLE_SPEED)

# Retry und Exit Bildschirm anzeigen
def show_end_screen():
    global score1, score2  # Global deklarieren, bevor sie verwendet werden
    font_end = pygame.font.SysFont(None, WIDTH // 30)  # Kleinere Schriftgröße
    retry_text = font_end.render("Retry", True, WHITE)
    exit_text = font_end.render("Exit", True, WHITE)

    # Buttongrößen anpassen (kleiner machen)
    retry_rect = pygame.Rect(WIDTH // 2 - retry_text.get_width() // 2 - 10, HEIGHT // 2, retry_text.get_width() + 20, retry_text.get_height() + 20)
    exit_rect = pygame.Rect(WIDTH // 2 - exit_text.get_width() // 2 - 10, HEIGHT // 2 + retry_text.get_height() + 40, exit_text.get_width() + 20, exit_text.get_height() + 20)

    option_selected = 0  # 0 für Retry, 1 für Exit
    while True:
        WIN.fill(BLACK)
        # Punktestand und Endbildschirm
        score_end = font_end.render(f"{score1}:{score2}", True, WHITE)
        WIN.blit(score_end, (WIDTH // 2 - score_end.get_width() // 2, HEIGHT // 4))
        
        # Optionen anzeigen
        if option_selected == 0:
            pygame.draw.rect(WIN, HIGHLIGHT_COLOR, retry_rect)  # Hervorhebung der Schaltfläche
        else:
            pygame.draw.rect(WIN, WHITE, retry_rect, 3)  # Normale Schaltfläche ohne Hervorhebung
        # Texte mittig im Button
        WIN.blit(retry_text, (retry_rect.centerx - retry_text.get_width() // 2, retry_rect.centery - retry_text.get_height() // 2))
        
        if option_selected == 1:
            pygame.draw.rect(WIN, HIGHLIGHT_COLOR, exit_rect)  # Hervorhebung der Schaltfläche
        else:
            pygame.draw.rect(WIN, WHITE, exit_rect, 3)  # Normale Schaltfläche ohne Hervorhebung
        # Texte mittig im Button
        WIN.blit(exit_text, (exit_rect.centerx - exit_text.get_width() // 2, exit_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option_selected = 0
                elif event.key == pygame.K_DOWN:
                    option_selected = 1
                elif event.key == pygame.K_RETURN:
                    if option_selected == 0:
                        # Spiel zurücksetzen
                        reset_ball()
                        score1, score2 = 0, 0
                        return  # Spiel fortsetzen
                    elif option_selected == 1:
                        pygame.quit()
                        sys.exit()

# Initialisierung
reset_ball()

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()

    if not game_over:
        move_paddles()
        game_over = update_ball()

    draw()
    pygame.display.flip()
    clock.tick(FPS)

    if game_over:
        # Zeige das Ende des Spiels und die Auswahlmöglichkeiten
        show_end_screen()
