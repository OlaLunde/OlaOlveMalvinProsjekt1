import tkinter as tk
import random
import platform

isMac = False


if platform.system() == "Darwin":
    isMac = True

if isMac:
    try:
        from tkmacosx import Button as MacButton
    except ImportError as e:
        print("Her er noe feil", e)
        print("MacOS brukere må installere følgende i konsollen: pip install tkmacosx")
        exit()


COLOURS = ["red", "blue", "green", "yellow", "orange", "purple"]
secret_code = [random.choice(COLOURS) for _ in range(4)]
number_attempts = 10

class Mastermindgame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")

        self.guess_count = 0
    
        self.guess = []
        self.chosen_colour_button = []  
        
        # Lager en tk ramme som skal inneholde tidligere gjetninger
        self.hist_frame = tk.Frame(root)
        self.hist_frame.pack(side=tk.TOP, pady=10)

        # navngir rammen laget ovenfor med tk label
        self.hist_label = tk.Label(self.hist_frame, text="Tidligere forsøk:", font=("Helvetica", 12, "bold italic"), 
            fg="black",
            padx=9,  
            pady=3,   )
        self.hist_label.pack()

        # lager en tk ramme inni hoved rammen
        self.hist_list = tk.Frame(self.hist_frame)
        self.hist_list.pack()

        # navngir root med tk label
        self.introduction = tk.Label(root, text="Velg fire farger og trykk på sjekk gjetning", font=("Helvetica", 12, "bold"),  
            fg="black", 
            padx=7,  
            pady=3,)
        self.introduction.pack(pady=10)

        # lager en ramme for fargene man kan velge i root
        self.coloursbuttons_frame = tk.Frame(root)
        self.coloursbuttons_frame.pack()

        # oppretter fargeknappene
        for colour in COLOURS:
            if isMac:
                button_class = MacButton
                width, height = 50, 50
            else:
                button_class = tk.Button
                width, height = 5, 2

            button = button_class(
                self.coloursbuttons_frame,
                bg=colour,
                relief="solid",
                borderwidth=1,
                width=width,
                height=height,
                command=lambda f=colour: self.add_colour(f)
            )
            button.pack(side=tk.LEFT, padx=8, pady=8)

        # Ramme for valgte farger
        self.chosen_colour_frame = tk.Frame(root)
        self.chosen_colour_frame.pack(pady=10)

        # Ramme for de to knappene: sjekk gjetning og spill igjen
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        if isMac:
            check_button_class = MacButton
            width = 100
        else:
            check_button_class = tk.Button
            width = 15


        # Knappen som sjekker gjetningen
        self.check_button = check_button_class(
            self.control_frame,
            text="Sjekk Gjetning",
            command=self.check_guess,
            font=("Helvetica", 12, "bold"), 
            bg="light gray", 
            fg="black",  
            width=width,
            activebackground="white",  
            activeforeground="black",  
            relief="raised",  
            borderwidth=2  
        )
        self.check_button.pack(side=tk.LEFT, padx=5, pady=1) 

        # tilbakemelding/resultat på sjekk gjetningen
        self.result_label = tk.Label(
            root,
            text="",  
            font=("Helvetica", 12, "bold"),  
            fg="red", 
            
        )
        self.result_label.pack(pady=10)

        # spill igjen knapp

        if isMac:
            play_again_button_class = MacButton
            width = 120
        else:
            play_again_button_class = tk.Button
            width = 20
        
        self.play_again_button = play_again_button_class(
        self.control_frame,
        text="Spill Igjen",
        command=self.reset_game,
        font=("Helvetica", 12, "bold"),
        bg="light gray",
        fg="black",
        width=width,
        activebackground="white",
        activeforeground="black",
        relief="raised",
        borderwidth=2
        )
        self.play_again_button.pack(side=tk.LEFT, padx=5, pady=1)


    def add_colour(self, colour):
        if len(self.guess) < 4:
            self.guess.append(colour)
            
            if isMac:
                button_class = MacButton
                width, height = 50, 50
            else:
                button_class = tk.Button
                width, height = 5, 2

            # oppretter knapp for valgt farge slik at den kan fjernes
            colour_button = button_class(
                self.chosen_colour_frame,
                bg=colour,
                relief="solid",
                borderwidth=1
            )
            colour_button.config(
                width=width,
                height=height,
                command=lambda fb=colour_button, f=colour: self.remove_colour(fb, f)
            )
            colour_button.pack(side=tk.LEFT, padx=5)
            self.chosen_colour_button.append(colour_button)

    # gjør det mulig å fjerne valgt farge
    def remove_colour(self, button, colour):
        button.destroy()
        if colour in self.guess:
            self.guess.remove(colour)

    def check_guess(self):
        if len(self.guess) != 4:
            self.result_label.config(text="Velg fire farger før du sjekker.")
            return

        correct_placement = sum(1 for i in range(4) if self.guess[i] == secret_code[i])
        correct_colour = sum(min(self.guess.count(f), secret_code.count(f)) for f in set(self.guess)) - correct_placement

        # Legg gjetningen til i historikken
        self.add_in_history(self.guess, correct_placement, correct_colour)


        # Vinn eller taper melding
        if correct_placement == 4:
            self.result_label.config(text="Gratulerer! Du gjettet koden riktig!")
            self.check_button.config(state=tk.DISABLED)

        else:
            self.guess_count += 1
            if self.guess_count >= number_attempts:
                self.result_label.config(
                    text=f"Beklager, du har brukt opp alle forsøkene. Koden var: {secret_code}"
                )
                self.check_button.config(state=tk.DISABLED)

            else:
                # Nullstill for ny gjetning
                self.guess = []
                for button in self.chosen_colour_button:
                    button.destroy()
                self.chosen_colour_button.clear()

    def add_in_history(self, guess, correct_placement, correct_colour):
    # Lag en ny ramme for hver gjetning
        guess_frame = tk.Frame(self.hist_list)
        guess_frame.pack(pady=2, fill=tk.X)

    # lager en ramme for "riktig farge" til venstre
        correct_colour_frame = tk.Frame(guess_frame)
        correct_colour_frame.pack(side=tk.LEFT, padx=10)

    # Etikett for riktig farge (venstre)
        correct_colour_label = tk.Label(
            correct_colour_frame, 
            text=f"Riktig farge: {correct_colour}", 
            font=("Helvetica", 10, "bold"),
            fg="green"
        )
        correct_colour_label.pack()

    # lager en ramme for de gjettede fargene i midten
        colourbox_frame = tk.Frame(guess_frame)
        colourbox_frame.pack(side=tk.LEFT, expand=True)

    # Vis farger for gjetningen som større bokser
        for colour in guess:
            colourbox = tk.Label(colourbox_frame, bg=colour, width=2, height=1, relief="solid", borderwidth=1)
            colourbox.pack(side=tk.LEFT, padx=3)

    # lager en ramme for "riktig plassering" til venstre
        correct_placement_frame = tk.Frame(guess_frame)
        correct_placement_frame.pack(side=tk.RIGHT, padx=10)

    # Etikett for riktig plassering (høyre)
        correct_placement_label = tk.Label(
            correct_placement_frame, 
            text=f"Riktig plassering: {correct_placement}", 
            font=("Helvetica", 10, "bold"),
            fg="blue"
        )
        correct_placement_label.pack()

    # lager en strek mellom gjetningene
        separator = tk.Frame(self.hist_list, height=1, bd=1, relief="sunken", bg="black")
        separator.pack(fill=tk.X, pady=3)
        
    def reset_game(self):
        global secret_code
        secret_code = [random.choice(COLOURS) for _ in range(4)]

        self.guess_count = 0
        self.guess = []

        for button in self.chosen_colour_button:
            button.destroy()
        self.chosen_colour_button.clear()

        # fjerner alle widgets fra historikken
        for widget in self.hist_list.winfo_children():
            widget.destroy()

        self.result_label.config(text="")

        # reaktiverer sjekk gjetning knapp
        self.check_button.config(state=tk.NORMAL)


root = tk.Tk()
app = Mastermindgame(root)
root.mainloop()
