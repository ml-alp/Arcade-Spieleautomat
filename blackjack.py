import tkinter as tk
import random


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1F1F1F")

        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = []

        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.player_wins = 0
        self.dealer_wins = 0
        self.current_option = 0  # 0: Hit, 1: Stand, 2: Quit

        self.game_active = True  # Verhindert Aktionen bei Sieg/Niederlage

        self.create_ui()
        self.new_game()

        # Tastatursteuerung
        self.root.bind("<Left>", lambda _: self.change_option(-1))
        self.root.bind("<Right>", lambda _: self.change_option(1))
        self.root.bind("<Return>", self.select_option)
        self.root.bind("q", lambda _: self.root.quit())

    def create_ui(self):
        # Frame für das gesamte Layout
        self.main_frame = tk.Frame(self.root, bg="#1F1F1F")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Überschrift
        self.title_label = tk.Label(self.main_frame, text="Blackjack", font=("Arial", 48, "bold"), bg="#1F1F1F", fg="white")
        self.title_label.pack(pady=20)

        # Punktestand
        self.score_label = tk.Label(
            self.main_frame,
            text=f"Spieler: {self.player_wins} | Dealer: {self.dealer_wins}",
            font=("Arial", 24),
            bg="#1F1F1F",
            fg="white"
        )
        self.score_label.pack()

        # Dealer-Bereich
        self.dealer_frame = tk.Frame(self.main_frame, bg="#1F1F1F")
        self.dealer_frame.pack(pady=20)

        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer:", font=("Arial", 24), bg="#1F1F1F", fg="white")
        self.dealer_label.grid(row=0, column=0, sticky='w')

        self.dealer_cards_label = tk.Label(self.dealer_frame, text="", font=("Courier", 22), bg="#1F1F1F", fg="white")
        self.dealer_cards_label.grid(row=1, column=0, sticky='w')

        self.dealer_score_label = tk.Label(self.dealer_frame, text="Summe: ?", font=("Arial", 20), bg="#1F1F1F", fg="white")
        self.dealer_score_label.grid(row=2, column=0, sticky='w')

        # Spieler-Bereich
        self.player_frame = tk.Frame(self.main_frame, bg="#1F1F1F")
        self.player_frame.pack(pady=50)

        self.player_label = tk.Label(self.player_frame, text="Spieler:", font=("Arial", 24), bg="#1F1F1F", fg="white")
        self.player_label.grid(row=0, column=0, sticky='w')

        self.player_cards_label = tk.Label(self.player_frame, text="", font=("Courier", 22), bg="#1F1F1F", fg="white")
        self.player_cards_label.grid(row=1, column=0, sticky='w')

        self.player_score_label = tk.Label(self.player_frame, text="Summe: 0", font=("Arial", 20), bg="#1F1F1F", fg="white")
        self.player_score_label.grid(row=2, column=0, sticky='w')

        # Steuerung
        self.button_frame = tk.Frame(self.main_frame, bg="#1F1F1F")
        self.button_frame.pack(pady=30)

        self.buttons = [
            tk.Label(self.button_frame, text="Ziehen", font=("Arial", 16), bg="#4CAF50", fg="white", width=12, height=2),
            tk.Label(self.button_frame, text="Passen", font=("Arial", 16), bg="#2196F3", fg="white", width=12, height=2),
            tk.Label(self.button_frame, text="Verlassen", font=("Arial", 16), bg="red", fg="white", width=12, height=2)
        ]

        for button in self.buttons:
            button.pack(side="left", padx=20)

        # Statusnachricht
        self.status_label = tk.Label(self.main_frame, text="", font=("Arial", 20), bg="#1F1F1F", fg="white")
        self.status_label.pack(pady=20)

        self.update_buttons()

    def new_game(self):
        self.deck = [f"{rank}{suit}" for rank in self.ranks for suit in self.suits]
        random.shuffle(self.deck)

        self.player_hand = []
        self.dealer_hand = []
        self.game_active = True
        self.status_label.config(text="")  # Statusmeldung zurücksetzen

        self.player_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())

        self.update_ui()

        # Überprüfen, ob der Spieler direkt Blackjack hat
        if self.calculate_score(self.player_hand) == 21:
            self.status_label.config(text="Blackjack! Spieler gewinnt!", fg="green")
            self.end_round(player_win=True)

    def update_ui(self, reveal_dealer=False):
        self.player_cards_label.config(text=" ".join(self.player_hand))
        self.player_score_label.config(text=f"Summe: {self.calculate_score(self.player_hand)}")

        if reveal_dealer:
            self.dealer_cards_label.config(text=" ".join(self.dealer_hand))
            self.dealer_score_label.config(text=f"Summe: {self.calculate_score(self.dealer_hand)}")
        else:
            self.dealer_cards_label.config(text=f"{self.dealer_hand[0]} ??")
            self.dealer_score_label.config(text="Summe: ?")

        # Punktestand aktualisieren
        self.score_label.config(text=f"Spieler: {self.player_wins} | Dealer: {self.dealer_wins}")

    def reveal_dealer_cards(self):
        self.update_ui(reveal_dealer=True)

    def hit(self):
        if not self.game_active:
            return

        self.player_hand.append(self.deck.pop())
        self.update_ui()

        if self.calculate_score(self.player_hand) == 21:
            self.status_label.config(text="Blackjack! Spieler gewinnt!", fg="green")
            self.end_round(player_win=True)
        elif self.calculate_score(self.player_hand) > 21:
            self.status_label.config(text="Spieler überzogen! Dealer gewinnt.", fg="red")
            self.end_round(player_win=False)

    def stand(self):
        if not self.game_active:
            return

        self.reveal_dealer_cards()

        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            self.update_ui(reveal_dealer=True)
            self.root.update()
            self.root.after(500)

        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.status_label.config(text="Spieler gewinnt!", fg="green")
            self.end_round(player_win=True)
        elif player_score < dealer_score:
            self.status_label.config(text="Dealer gewinnt.", fg="red")
            self.end_round(player_win=False)
        else:
            self.status_label.config(text="Unentschieden!", fg="orange")
            self.end_round(player_win=None)

    def end_round(self, player_win):
        self.game_active = False
        if player_win is True:
            self.player_wins += 1
        elif player_win is False:
            self.dealer_wins += 1

        self.root.after(3000, self.new_game)

    def calculate_score(self, hand):
        score = 0
        ace_count = hand.count('A')
        for card in hand:
            if card[:-1] == 'A':
                score += 11
            elif card[:-1] in ['K', 'Q', 'J']:
                score += 10
            else:
                score += int(card[:-1])

        # Asse korrekt behandeln
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1

        return score

    def change_option(self, direction):
        if self.game_active:
            self.current_option = (self.current_option + direction) % len(self.buttons)
            self.update_buttons()

    def update_buttons(self):
        for i, button in enumerate(self.buttons):
            if i == self.current_option:
                button.config(bg="#5A5A5A")  # Hervorheben des aktuell ausgewählten Buttons
            else:
                button.config(bg="#333333")

    def select_option(self, event=None):
        if not self.game_active:
            return

        if self.current_option == 0:  # Hit
            self.hit()
        elif self.current_option == 1:  # Stand
            self.stand()
        elif self.current_option == 2:  # Quit
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
