import tkinter as tk
import subprocess
import os


def start_program1():
    subprocess.Popen(["python", "Games\TikTakToe_mit_Pfeiltasten.py"])
    os.system('qjoypad "tik_tak_toe"')

def start_program2():
    subprocess.Popen(["python", "Games\slots.py"])
    os.system('qjoypad "slots"')

def start_program3():
    subprocess.Popen(["python", "Games\snake.py"])
    os.system('qjoypad "snake"')

def start_program4():
    subprocess.Popen(["python", "Games\Tetris.py"])
    os.system('qjoypad "tetris"')

def start_program5():
    subprocess.Popen(["python", "Games\pong.py"])
    os.system('qjoypad "pong"')

def start_program6():
    subprocess.Popen(["python", "Games\SpaceInvaders.py"])
    os.system('qjoypad "invaders"')

def close_program():
    root.destroy()

def toggle_fullscreen(event=None):
    root.state = not root.state  
    root.attributes("-fullscreen", root.state)
    return "break"

def end_fullscreen(event=None):
    root.state = False
    root.attributes("-fullscreen", False)
    return "break"

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def focus_prev_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"

def focus_widget_below(event):
    current_widget = event.widget
    parent = current_widget.master
    children = parent.winfo_children()
    index = children.index(current_widget)
    next_row_index = index + 3  
    if next_row_index < len(children):
        children[next_row_index].focus()
    return "break"

def focus_widget_above(event):
    current_widget = event.widget
    parent = current_widget.master
    children = parent.winfo_children()
    index = children.index(current_widget)
    previous_row_index = index - 3 
    if previous_row_index >= 0:
        children[previous_row_index].focus()
    return "break"

def select_widget(event):
    focused_widget = root.focus_get()
    focused_widget.invoke()
    return "break"

def on_focus_in(event):
    event.widget.config(bg="lightgrey", fg="black", highlightbackground="lightgrey", highlightthickness=2)

def on_focus_out(event):
    if event.widget == button1:
        event.widget.config(bg="green", fg="white", highlightbackground="green", highlightthickness=0)
    elif event.widget == button2:
        event.widget.config(bg="blue", fg="white", highlightbackground="blue", highlightthickness=0)
    elif event.widget == button3:
        event.widget.config(bg="green", fg="black", highlightbackground="green", highlightthickness=0)
    elif event.widget == button4:
        event.widget.config(bg="blue", fg="white", highlightbackground="blue", highlightthickness=0)
    elif event.widget == button5:
        event.widget.config(bg="green", fg="black", highlightbackground="green", highlightthickness=0)
    elif event.widget == button6:
        event.widget.config(bg="blue", fg="white", highlightbackground="blue", highlightthickness=0)

# Hauptfenster erstellen
root = tk.Tk()
root.title("Arcade")
root.state = False


# Bildschirmauflösung ermitteln
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Vollbildmodus aktivieren
root.attributes("-fullscreen", True)
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)

# Hintergrundbild hinzufügen
background_image = tk.PhotoImage(file="background.png")  
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)


# Rahmen für die Inhalte erstellen, passt sich der Bildschirmauflösung an
frame = tk.Frame(root, bg="black")
frame.place(width=screen_width * 0.6, height=screen_height * 0.4, relx=0.5, rely=0.5, anchor="center")

# Überschrift hinzufügen
header = tk.Label(frame, text="Hausmesse 19.11.2024 --- Retro Acarde Games",
                  font=("Press Start 2P", 18, "bold"), fg="cyan", bg="black")
header.grid(row=0, column=0, columnspan=3, pady=15)

# Buttons für das Starten der Programme erstellen
button1 = tk.Button(frame, text="Tic Tac Toe", font=("Press Start 2P", 14, "bold"), bg="green", fg="black", highlightthickness=0, command=start_program1, height=2, width=20)
button2 = tk.Button(frame, text="Slots", font=("Press Start 2P", 14, "bold"), bg="blue", fg="white", highlightthickness=0, command=start_program2, height=2, width=20)
button3 = tk.Button(frame, text="Snake", font=("Press Start 2P", 14, "bold"), bg="green", fg="black", highlightthickness=0, command=start_program3, height=2, width=20)
button4 = tk.Button(frame, text="Tetris", font=("Press Start 2P", 14, "bold"), bg="blue", fg="white", highlightthickness=0, command=start_program4, height=2, width=20)
button5 = tk.Button(frame, text="Pong", font=("Press Start 2P", 14, "bold"), bg="green", fg="black", highlightthickness=0, command=start_program5, height=2, width=20)
button6 = tk.Button(frame, text="Space Invaders", font=("Press Start 2P", 14, "bold"), bg="blue", fg="white", highlightthickness=0, command=start_program6, height=2, width=20)

# Positioniere Buttons im Grid-Layout
button1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
button2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
button3.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
button4.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
button5.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
button6.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

# Konfiguriere die Grid-Optionen
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Fokus auf den ersten Button setzen
button1.focus_set()

# Event-Bindings
root.bind("<Left>", focus_prev_widget)
root.bind("<Right>", focus_next_widget)
root.bind("<Down>", focus_widget_below)
root.bind("<Up>", focus_widget_above)
root.bind("<Return>", select_widget)

# Event-Bindings für Focus-In und Focus-Out
buttons = [button1, button2, button3, button4, button5, button6]
for button in buttons:
    button.bind("<FocusIn>", on_focus_in)
    button.bind("<FocusOut>", on_focus_out)

# Hauptschleife starten
root.mainloop()
