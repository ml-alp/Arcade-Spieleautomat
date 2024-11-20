import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import os

class SlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")

        # Hintergrundbild laden und skalieren
        self.bg_image = Image.open("casino.png")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Canvas für Hintergrundbild erstellen
        self.canvas = tk.Canvas(root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Hintergrundbild auf dem Canvas anzeigen
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image_tk)

        # Laden und Skalieren der Symbole
        self.symbol_size = (150, 150)
        self.symbols = [
            ImageTk.PhotoImage(Image.open("symbol1.png").resize(self.symbol_size, Image.LANCZOS)),
            ImageTk.PhotoImage(Image.open("symbol2.png").resize(self.symbol_size, Image.LANCZOS)),
            ImageTk.PhotoImage(Image.open("symbol3.png").resize(self.symbol_size, Image.LANCZOS)),
            ImageTk.PhotoImage(Image.open("symbol4.png").resize(self.symbol_size, Image.LANCZOS)),
            ImageTk.PhotoImage(Image.open("symbol5.png").resize(self.symbol_size, Image.LANCZOS))
        ]

        # Initialisiere Pygame für die Audio-Wiedergabe
        pygame.mixer.init()
        pygame.mixer.music.load("background_music_slots.mp3")
        pygame.mixer.music.play(-1)

        # Spin-Sound und Gewinn-Sound laden
        self.spin_sound = pygame.mixer.Sound("spin_sound.mp3")
        self.win_sound = pygame.mixer.Sound("win_sound.mp3")

        # Erstellen der Frames für die Slot-Labels
        self.slot_frames = []
        for col in range(3):
            column_frames = []
            for row in range(3):
                frame = tk.Frame(root, bg='white', highlightthickness=8, bd=0)  # Hintergrund auf weiß, kein Rand
                if row == 1:
                    frame.config(highlightbackground='red')
                else:
                    frame.config(highlightbackground='black')

                frame.place_forget()  # Frame zuerst nicht anzeigen
                column_frames.append((frame, tk.Label(frame, image=random.choice(self.symbols), bg='white')))
            self.slot_frames.append(column_frames)

        # Fenster maximieren und zentrieren
        self.root.attributes('-fullscreen', True)
        self.center_window()

        # Gewinnanzeige
        self.win_label = tk.Label(root, text="", bg="black", font=("Arial", 36, "bold"), fg="darkgreen")
        self.win_label.place(relx=0.5, rely=0.05, anchor='n')

        # Quit-Button
        self.quit_button = tk.Button(root, text="Quit", bg="darkred", fg="white", font=("Arial", 16, "bold"), command=self.confirm_quit)
        self.quit_button.place(relx=1.0, rely=1.0, anchor='se', x=-30, y=-30)

        # Spin-Button
        self.spin_button = tk.Button(root, text="Spin", bg="green", fg="white", font=("Arial", 16, "bold"), command=self.handle_spin)
        self.spin_button.place(relx=0.5, rely=0.9, anchor='center')

        # Leertaste für Spin
        self.root.bind("<space>", lambda event: self.handle_spin())

        # Q für Beenden
        self.root.bind("q", lambda event: self.confirm_quit())

        # Variable für den Animationszustand
        self.spinning = False

    def center_window(self):
        # Canvas ist jetzt das gesamte Fenster
        self.canvas.config(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())

        # Zentrieren der Slots in der Mitte
        slot_width = self.symbol_size[0] + 40
        slot_height = self.symbol_size[1] + 40
        total_width = 3 * slot_width
        total_height = 3 * slot_height
        start_x = (self.root.winfo_screenwidth() - total_width) // 2
        start_y = (self.root.winfo_screenheight() - total_height) // 2
        for col in range(3):
            for row in range(3):
                x = start_x + col * slot_width
                y = start_y + row * slot_height
                self.slot_frames[col][row][0].place(x=x, y=y)
                self.slot_frames[col][row][1].pack()

    def handle_spin(self):
        if not self.spinning:
            self.spinning = True
            self.spin_button.config(state=tk.DISABLED)  # Spin-Button deaktivieren
            self.spin_sound.play()
            self.spin()

    def spin(self):
        # Anzahl der Schritte für die Animation
        steps = 20
        delay = 50

        def animate_step(step):
            if step < steps:
                for col in range(3):
                    # Verschieben der Symbole nach unten
                    for row in range(2, 0, -1):
                        self.slot_frames[col][row][1].config(image=self.slot_frames[col][row-1][1].cget('image'))

                    # Neues Symbol oben hinzufügen
                    new_symbol = random.choice(self.symbols)
                    self.slot_frames[col][0][1].config(image=new_symbol)

                self.root.after(delay, animate_step, step + 1)
            else:
                self.check_win()  # Überprüfen auf Gewinn

        # Start der Animation
        animate_step(0)

    def check_win(self):
        center_symbols = [self.slot_frames[col][1][1].cget('image') for col in range(3)]
        if center_symbols[0] == center_symbols[1] == center_symbols[2]:
            self.win_label.config(text="Gewonnen!")
            self.win_sound.play()  # Gewinn-Sound abspielen
            pygame.mixer.music.pause()  # Hintergrundmusik pausieren
            self.blink_win_label()  # Gewinntext blinken lassen
            # Setze die Spinsperre für 5 Sekunden
            self.root.after(5000, self.enable_spin_button)  # Reaktivieren des Spin-Buttons nach 5 Sekunden
        else:
            self.win_label.config(text="")  # Kein Gewinn, keine Anzeige
            pygame.mixer.music.unpause()  # Hintergrundmusik fortsetzen
            # Setze die Spinsperre für 1,5 Sekunden
            self.root.after(350, self.enable_spin_button)  # Reaktivieren des Spin-Buttons nach 1,5 Sekunden

    def blink_win_label(self):
        # Blinken-Effekte für den Gewinntext
        def blink_step(step):
            if step < 10:
                # Alternieren der Farbe
                current_fg = 'darkgreen' if step % 2 == 0 else 'yellow'
                self.win_label.config(fg=current_fg)
                self.root.after(300, blink_step, step + 1)  # Blinken alle 300 ms
            else:
                # Zurück zur ursprünglichen Farbe nach dem Blinken
                self.win_label.config(fg='darkgreen')
                pygame.mixer.music.unpause()

        # Start des Blinkens
        blink_step(0)

    def enable_spin_button(self):
        self.spin_button.config(state=tk.NORMAL)  # Spin-Button wieder aktivieren
        self.spinning = False  # Erlaube weitere Spins

    def confirm_quit(self, event=None):
        pygame.mixer.music.stop()
        self.root.destroy()
        os.system('qjoypad "main"')

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachine(root)
    root.mainloop()

