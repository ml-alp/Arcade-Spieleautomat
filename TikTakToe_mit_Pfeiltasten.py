import tkinter as tk
from PIL import Image, ImageTk

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        # Vollbildmodus
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.current_player = "X"
        self.start_player = "X"  # Startspieler für das erste Spiel
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_row = 0
        self.current_col = 0
        self.quit_selected = False
        self.scores = {"X": 0, "O": 0}
        self.overlay_selected = 0  # Overlay-Auswahl (0 = Exit, 1 = Retry)

        self.create_widgets()
        self.create_buttons()
        self.highlight_current_cell()
        self.bind_keys()

        # Hintergrundbild setzen
        self.change_background('background_tiktaktoe.jpg')

    def create_widgets(self):
        # Canvas für Hintergrund
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Hintergrundbild auf Canvas platzieren
        self.background_image = Image.open('background_tiktaktoe.jpg')
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Frame für das Hauptspiel
        self.main_frame = tk.Frame(self.canvas, bg='lightgrey')
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Anzeige des Punktestands
        self.score_frame = tk.Frame(self.main_frame, bg='lightgrey')
        self.score_frame.grid(row=0, column=0)
        self.score_label = tk.Label(self.score_frame, text="X: 0   O: 0", font=('normal', 20), bg='lightgrey')
        self.score_label.pack()

        # Frame für das Spielfeld
        self.frame = tk.Frame(self.main_frame, bg='black')
        self.frame.grid(row=1, column=0, padx=20, pady=20)

        # Quit-Button unten rechts hinzufügen
        self.quit_button = tk.Button(self.root, text="X", bg="red", fg="white", font=('normal', 20), command=self.confirm_quit)
        self.quit_button.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

    def create_buttons(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.frame, text=" ", font=('normal', 40), width=5, height=2, bg='white', fg='black')
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

    def highlight_current_cell(self):
        for row in range(3):
            for col in range(3):
                if row == self.current_row and col == self.current_col and not self.quit_selected:
                    self.buttons[row][col].config(bg="lightblue")
                else:
                    self.buttons[row][col].config(bg="white")
        if self.quit_selected:
            self.quit_button.config(bg="lightblue")
        else:
            self.quit_button.config(bg="red")

    def move_player_X_up(self, event):
        if self.current_player == "X" and not self.quit_selected:
            if self.current_row > 0:
                self.current_row -= 1
                self.highlight_current_cell()

    def move_player_X_down(self, event):
        if self.current_player == "X" and not self.quit_selected:
            if self.current_row < 2:
                self.current_row += 1
                self.highlight_current_cell()

    def move_player_X_left(self, event):
        if self.current_player == "X" and not self.quit_selected:
            if self.current_col > 0:
                self.current_col -= 1
                self.highlight_current_cell()

    def move_player_X_right(self, event):
        if self.current_player == "X" and not self.quit_selected:
            if self.current_col < 2:
                self.current_col += 1
                self.highlight_current_cell()

    def move_player_O_up(self, event):
        if self.current_player == "O" and not self.quit_selected:
            if self.current_row > 0:
                self.current_row -= 1
                self.highlight_current_cell()

    def move_player_O_down(self, event):
        if self.current_player == "O" and not self.quit_selected:
            if self.current_row < 2:
                self.current_row += 1
                self.highlight_current_cell()

    def move_player_O_left(self, event):
        if self.current_player == "O" and not self.quit_selected:
            if self.current_col > 0:
                self.current_col -= 1
                self.highlight_current_cell()

    def move_player_O_right(self, event):
        if self.current_player == "O" and not self.quit_selected:
            if self.current_col < 2:
                self.current_col += 1
                self.highlight_current_cell()

    def select_cell(self, event):
        if not self.quit_selected:
            if self.buttons[self.current_row][self.current_col]["text"] == " ":
                self.buttons[self.current_row][self.current_col]["text"] = self.current_player
                self.board[self.current_row][self.current_col] = self.current_player
                if self.check_win(self.current_player):
                    self.show_win_message(self.current_player)
                elif self.check_draw():
                    self.show_draw_message()
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
                    self.highlight_current_cell()

    def update_score(self):
        self.score_label.config(text=f"X: {self.scores['X']}   O: {self.scores['O']}")

    def show_win_message(self, winner):
        self.show_overlay("Player {} wins!".format(winner))

        # Punkte aktualisieren
        self.scores[winner] += 1
        self.update_score()

    def show_draw_message(self):
        self.show_overlay("It's a draw!")

    def confirm_quit(self, event=None):
        self.show_overlay("Are you sure you want to quit?")

    def show_overlay(self, message):
        # Overlay für Meldung erstellen
        self.overlay_frame = tk.Frame(self.root, bg='lightgrey', bd=10, relief=tk.RIDGE)
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=200)

        self.message_label = tk.Label(self.overlay_frame, text=message, font=('normal', 20), bg='lightgrey')
        self.message_label.place(relx=0.5, rely=0.3, anchor="center")  # Nach oben verschoben

        self.retry_button = tk.Label(self.overlay_frame, text="Retry", font=('normal', 20), bg='lightgrey', bd=5, relief=tk.RAISED)
        self.retry_button.place(relx=0.5, rely=0.7, anchor="center", y=-30)  # Retry Button oben

        self.exit_button = tk.Label(self.overlay_frame, text="Exit", font=('normal', 20), bg='lightgrey', bd=5, relief=tk.RAISED)
        self.exit_button.place(relx=0.5, rely=0.7, anchor="center", y=30)  # Exit Button unten

        self.highlight_overlay_option()

        self.root.bind("<Up>", self.navigate_overlay_up)
        self.root.bind("<Down>", self.navigate_overlay_down)
        self.root.bind("<Return>", self.select_overlay_option)

        self.root.bind("w", self.navigate_overlay_up)
        self.root.bind("s", self.navigate_overlay_down)
        self.root.bind("a", self.navigate_overlay_left)
        self.root.bind("d", self.navigate_overlay_right)

    def navigate_overlay_up(self, event):
        self.overlay_selected = 1  # Retry
        self.highlight_overlay_option()

    def navigate_overlay_down(self, event):
        self.overlay_selected = 0  # Exit
        self.highlight_overlay_option()

    def navigate_overlay_left(self, event):
        # Optionale zusätzliche Navigation für andere Tasten (wenn gewünscht)
        pass

    def navigate_overlay_right(self, event):
        # Optionale zusätzliche Navigation für andere Tasten (wenn gewünscht)
        pass

    def select_overlay_option(self, event):
        if self.overlay_selected == 1:
            self.retry_game()
        else:
            self.exit_game()

    def highlight_overlay_option(self):
        if hasattr(self, 'retry_button') and hasattr(self, 'exit_button'):
            if self.overlay_selected == 1:
                self.retry_button.config(bg="lightblue")
                self.exit_button.config(bg="lightgrey")
            else:
                self.retry_button.config(bg="lightgrey")
                self.exit_button.config(bg="lightblue")

    def retry_game(self):
        self.overlay_frame.destroy()
        self.reset_game()

    def exit_game(self):
        self.overlay_frame.destroy()
        self.root.destroy()

    def reset_game(self):
        self.current_player = "O" if self.start_player == "X" else "X"
        self.start_player = self.current_player
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = " "
        self.current_row = 0
        self.current_col = 0
        self.quit_selected = False
        self.highlight_current_cell()
        self.bind_keys()

    def check_win(self, player):
        win = any(
            all(cell == player for cell in row) for row in self.board
        ) or any(
            all(self.board[r][c] == player for r in range(3)) for c in range(3)
        ) or all(
            self.board[i][i] == player for i in range(3)
        ) or all(
            self.board[i][2 - i] == player for i in range(3)
        )
        return win

    def check_draw(self):
        return all(cell in ['X', 'O'] for row in self.board for cell in row)

    def exit_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)

    def change_background(self, image_path):
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)

        # Entferne vorheriges Hintergrundbild, falls vorhanden
        if hasattr(self, 'canvas'):
            self.canvas.delete("all")
        else:
            self.canvas = tk.Canvas(self.root)
            self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        self.canvas.image = background_image

    def bind_keys(self):
        # Tastaturereignisse binden
        self.root.bind("<Up>", self.move_player_X_up)
        self.root.bind("<Down>", self.move_player_X_down)
        self.root.bind("<Left>", self.move_player_X_left)
        self.root.bind("<Right>", self.move_player_X_right)

        self.root.bind("w", self.move_player_O_up)
        self.root.bind("s", self.move_player_O_down)
        self.root.bind("a", self.move_player_O_left)
        self.root.bind("d", self.move_player_O_right)

        self.root.bind("<Return>", self.select_cell)
        self.root.bind("q", self.confirm_quit)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

