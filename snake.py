import tkinter as tk
import random
import pygame  # Importiere pygame für Musik und Soundeffekte

# Globale Variablen für das Spiel
SEG_SIZE = 20
IN_GAME = True
SCORE = 0
WIDTH = 500  # Breite des Spielfelds
HEIGHT = 500  # Höhe des Spielfelds
HIGHSCORE_FILE = 'highscore.txt'  # Datei für den Highscore

# Initialisiere pygame
pygame.init()
pygame.mixer.init()

# Lade Musik und Soundeffekte
pygame.mixer.music.load('background_music1.mp3')  # Hintergrundmusik
eat_sound = pygame.mixer.Sound('eating.mp3')  # Soundeffekt für Essen

# Klasse für die Snake
class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.segments = [(20, 20)]
        self.dx = SEG_SIZE
        self.dy = 0
        self.food = self.set_food()

    def move(self):
        global SCORE
        head_x, head_y = self.segments[0]
        new_head = (head_x + self.dx, head_y + self.dy)
        
        # Kollision mit Wänden
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return False

        # Kollision mit sich selbst
        if new_head in self.segments:
            return False

        self.segments = [new_head] + self.segments[:-1]

        # Wenn Essen gegessen wird
        if new_head == self.food:
            SCORE += 1
            self.segments.append(self.segments[-1])
            self.food = self.set_food()
            eat_sound.play()  # Spiele den Soundeffekt ab, wenn das Essen gegessen wird

        return True

    def change_direction(self, event):
        if event.keysym in ['Up', 'w'] and self.dy == 0:
            self.dx, self.dy = 0, -SEG_SIZE
        elif event.keysym in ['Down', 's'] and self.dy == 0:
            self.dx, self.dy = 0, SEG_SIZE
        elif event.keysym in ['Left', 'a'] and self.dx == 0:
            self.dx, self.dy = -SEG_SIZE, 0
        elif event.keysym in ['Right', 'd'] and self.dx == 0:
            self.dx, self.dy = SEG_SIZE, 0

    def set_food(self):
        while True:
            x = random.randint(0, (WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            y = random.randint(0, (HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            if (x, y) not in self.segments:
                return (x, y)

# Hauptklasse für das Spiel
class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Snake Game')

        # Vollbildmodus einstellen
        self.master.attributes('-fullscreen', True)

        # Bildschirmgröße ermitteln
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Mittelpunkt des Bildschirms berechnen
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Canvas erstellen
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.place(x=center_x - WIDTH // 2, y=center_y - HEIGHT // 2)

        # Score-Label erstellen
        self.score_label = tk.Label(self.master, text=f'Score: {SCORE}', font=('Helvetica', 16, 'bold'), bg='black', fg='white')
        self.score_label.pack(side=tk.TOP, pady=20)

        # Highscore-Label erstellen
        self.highscore = self.load_highscore()
        self.highscore_label = tk.Label(self.master, text=f'Highscore: {self.highscore}', font=('Helvetica', 16, 'bold'), bg='black', fg='white')
        self.highscore_label.pack(side=tk.TOP, pady=20)

        self.snake = Snake(self.canvas)

        self.start_music()
        self.draw_game()

        self.master.bind('<KeyPress>', self.snake.change_direction)
        self.game_loop()

    def start_music(self):
        pygame.mixer.music.play(-1)  # -1 bedeutet, dass die Musik in einer Endlosschleife läuft

    def draw_game(self):
        self.canvas.delete(tk.ALL)
        # Zeichne die Schlange
        for segment in self.snake.segments:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill='green')

        # Zeichne das Essen
        x, y = self.snake.food
        self.canvas.create_oval(x, y, x + SEG_SIZE, y + SEG_SIZE, fill='red')

    def game_loop(self):
        global IN_GAME
        if IN_GAME:
            if self.snake.move():
                self.draw_game()
                self.score_label.config(text=f'Score: {SCORE}')
                self.master.after(100, self.game_loop)
            else:
                IN_GAME = False
                self.show_game_over_dialog()

    def show_game_over_dialog(self):
        # Stoppe die Hintergrundmusik
        pygame.mixer.music.stop()

        # Überprüfe und speichere den Highscore
        if SCORE > self.highscore:
            self.highscore = SCORE
            self.save_highscore(self.highscore)

        self.canvas.delete(tk.ALL)
        self.score_label.config(text=f'Game Over! Score: {SCORE}')
        self.highscore_label.config(text=f'Highscore: {self.highscore}')
        
        self.retry_button = tk.Button(self.master, text="Retry", command=self.restart_game, bg='white', font=('Helvetica', 16), width=10, height=2)
        self.retry_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, bg='white', font=('Helvetica', 16), width=10, height=2)
        self.exit_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.current_button = self.retry_button
        self.highlight_button(self.current_button)

        self.master.bind('<KeyPress>', self.navigate_buttons)

    def highlight_button(self, button):
        button.config(bg='green')

    def unhighlight_button(self, button):
        button.config(bg='white')

    def navigate_buttons(self, event):
        if event.keysym in ['Up', 'Down']:
            self.unhighlight_button(self.current_button)
            if self.current_button == self.retry_button:
                self.current_button = self.exit_button
            else:
                self.current_button = self.retry_button
            self.highlight_button(self.current_button)
            self.current_button.focus_set()

    def restart_game(self):
        global IN_GAME, SCORE
        IN_GAME = True
        SCORE = 0
        self.snake = Snake(self.canvas)
        self.score_label.config(text=f'Score: {SCORE}')
        self.retry_button.destroy()
        self.exit_button.destroy()
        self.master.bind('<KeyPress>', self.snake.change_direction)
        self.start_music()  # Starte die Musik neu
        self.game_loop()

    def load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0

    def save_highscore(self, highscore):
        with open(HIGHSCORE_FILE, 'w') as file:
            file.write(str(highscore))

# Hauptfunktion zum Starten des Spiels
def main():
    root = tk.Tk()
    root.title('Snake Game')
    root.configure(bg='black')
    game = SnakeGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()

