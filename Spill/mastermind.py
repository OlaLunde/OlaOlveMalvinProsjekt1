import tkinter as tk
import random

# Tilgjengelige farger for spillet
COLOURS = ["red", "blue", "green", "yellow", "orange", "purple"]

# Generer en hemmelig kode
secret_code = [random.choice(COLOURS) for _ in range(4)]
number_attempts = 10

class Mastermindgame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")

        # Initialisering
        self.guess_count = 0
        self.guess = []
        self.chosen_colour_button = []  # Holder knappene for valgte farger
        
        # Ramme for tidligere gjetninger
        self.hist_frame = tk.Frame(root)
        self.hist_frame.pack(side=tk.TOP, pady=10)

        # Historikk label
        self.hist_label = tk.Label(self.hist_frame, text="Tidligere forsøk:", font=("Helvetica", 12, "bold italic"),  # Endrer font, størrelse, og stil
            fg="black", # Endrer bakgrunnsfargen
            padx=9,  # Legger til ekstra plass rundt teksten (horisontalt)
            pady=3,   )
        self.hist_label.pack()

        # Ramme for tidligere forsøk-liste
        self.hist_list = tk.Frame(self.hist_frame)
        self.hist_list.pack()

        # Lag hovedlayouten
        self.introduction = tk.Label(root, text="Velg fire farger og trykk på sjekk gjetning", font=("Helvetica", 12, "bold"),  # Endrer font, størrelse, og stil
            fg="black", # Endrer bakgrunnsfargen
            padx=7,  # Legger til ekstra plass rundt teksten (horisontalt)
            pady=3,)
        self.introduction.pack(pady=10)

        # Lag en ramme for fargevalg
        self.coloursbuttons_frame = tk.Frame(root)
        self.coloursbuttons_frame.pack()

        # Opprett fargeknappene
        for colour in COLOURS:
            button = tk.Button(self.coloursbuttons_frame, bg=colour, width=5, height=2, relief="solid", borderwidth=1,
                              command=lambda f=colour: self.add_colour(f))
            button.pack(side=tk.LEFT, padx=5)

        # Ramme for valgte farger
        self.chosen_colour_frame = tk.Frame(root)
        self.chosen_colour_frame.pack(pady=10)

        # Knapperamme for å sjekke gjetning og nullstille
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        # Sjekk-knapp med styling
        self.check_button = tk.Button(
            self.control_frame,
            text="Sjekk Gjetning",
            command=self.check_guess,
            font=("Helvetica", 12, "bold"),  # Større og fet tekst
            bg="light gray",  # Blå bakgrunnsfarge
            fg="black",  # Hvit tekstfarge
            activebackground="white",  # Mørk blå bakgrunn når knappen trykkes
            activeforeground="black",  # Hvit tekst når knappen trykkes
            width=10,  # Økt bredde
            height=2,  # Økt høyde
            relief="raised",  # Tredimensjonal effekt
            borderwidth=2  # Tykkere kant
        )
        self.check_button.pack(side=tk.LEFT, padx=5, pady=1)  # Ekstra avstand rundt knappen

        # Tilbakemelding med styling
        self.result_label = tk.Label(
            root,
            text="",  # Start med tom tekst
            font=("Helvetica", 12, "bold"),  # Fet tekst
            fg="red",  # Rød tekstfarge
            
        )
        self.result_label.pack(pady=10)  # Avstand rundt etiketten

    def add_colour(self, colour):
        # Legg til farge hvis det er plass i gjettningen
        if len(self.guess) < 4:
            self.guess.append(colour)
            # Opprett en knapp for den valgte fargen
            # Definer `farge_knapp` før vi bruker den i lambda-funksjonen
            colour_button = tk.Button(self.chosen_colour_frame, bg=colour, width=5, height=2)
            colour_button.config(command=lambda fb=colour_button, f=colour: self.remove_colour(fb, f))
            colour_button.pack(side=tk.LEFT, padx=5)
            self.chosen_colour_button.append(colour_button)

    def remove_colour(self, button, colour):
        # Fjern valgt farge både fra GUI og fra gjett-listen
        button.destroy()
        self.guess.remove(colour)

    def check_guess(self):
        if len(self.guess) != 4:
            self.result_label.config(text="Velg fire farger før du sjekker.")
            return

        # Sjekk korrekt plassering
        correct_placement = sum(1 for i in range(4) if self.guess[i] == secret_code[i])

        # Sjekk riktige farger, men feil plassering
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

    # Lag en ramme for "Riktig farge" til venstre
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

    # Lag en ramme for fargeboksene i midten
        colourbox_frame = tk.Frame(guess_frame)
        colourbox_frame.pack(side=tk.LEFT, expand=True)

    # Vis farger for gjetningen som større bokser
        for colour in guess:
            colourbox = tk.Label(colourbox_frame, bg=colour, width=2, height=1, relief="solid", borderwidth=1)
            colourbox.pack(side=tk.LEFT, padx=3)

    # Lag en ramme for "Riktig plassering" til høyre
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

    # Legg til en horisontal strek for å skille hver gjetning
        separator = tk.Frame(self.hist_list, height=1, bd=1, relief="sunken", bg="black")
        separator.pack(fill=tk.X, pady=3)


# Start spillet
root = tk.Tk()
app = Mastermindgame(root)
root.mainloop()
