import tkinter as tk
import random
import platform
import requests as req

isMac = False

URL = "https://rasmusweb.no/hs.php"
GameID = "mastermind"

if platform.system() == "Darwin":
    isMac = True

if isMac:
    try:
        from tkmacosx import Button as MacButton
    except ImportError as e:
        print("Her er noe feil", e)
        print("MacOS brukere må installere følgende i konsollen: pip install tkmacosx")
        exit()

# Tilgjengelige farger for spillet
COLOURS = ["red", "blue", "green", "yellow", "orange", "purple"]

# Generer en hemmelig kode
secret_code = [random.choice(COLOURS) for _ in range(4)]
number_attempts = 10

class Mastermindgame:
    def __init__(self, root):
        self.resultat = None

        self.player_name_frame = tk.Frame(root)
        self.player_name_frame.pack(pady=10)
        
        self.name_label = tk.Label(self.player_name_frame, text="Skriv inn navnet ditt:", font=("Helvetica", 12))
        self.name_label.pack(side=tk.LEFT, padx=5)

        self.name_entry = tk.Entry(self.player_name_frame, font=("Helvetica", 12))
        self.name_entry.pack(side=tk.LEFT, padx=5)



        self.start_button = tk.Button(
            self.player_name_frame, 
            text="Start Spill", 
            command=self.start_game,
            font=("Helvetica", 12, "bold"),
            bg="light gray",
            fg="black"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.root = root
        self.root.title("Mastermind")

        self.hs_frame = tk.Frame(root)
        self.hs_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")  # Flytter til toppen

        self.hs_label = tk.Label(self.hs_frame, text="Highscore (Topp 5)", font=("Helvetica", 12, "bold"))
        self.hs_label.pack()

        self.hs_list = tk.Frame(self.hs_frame)
        self.hs_list.pack()

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
        # Problemet ligger i denne delen
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

        # Knapperamme for å sjekke gjetning og nullstille
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        if isMac:
            width = 40
        else:
            width = 15


        # Sjekk-knapp med styling
        self.check_button = tk.Button(
            self.control_frame,
            text="Sjekk Gjetning",
            command=self.check_guess,
            font=("Helvetica", 12, "bold"), 
            bg="light gray", 
            fg="black",  
            width=width,
            activebackground="white",  
            activeforeground="black",  
            relief="raised",  # Tredimensjonal effekt
            borderwidth=2  
        )
        self.check_button.pack(side=tk.LEFT, padx=5, pady=1)  # Ekstra avstand rundt knappen

        # Tilbakemelding med styling
        self.result_label = tk.Label(
            root,
            text="",  
            font=("Helvetica", 12, "bold"),  
            fg="red",  # Rød tekstfarge
            
        )
        self.result_label.pack(pady=10)  # Avstand rundt etiketten

        self.play_again_button = tk.Button(
        self.control_frame,
        text="Spill Igjen",
        command=self.reset_game,
        font=("Helvetica", 12, "bold"),
        bg="light gray",
        fg="black",
        width=20,
        activebackground="white",
        activeforeground="black",
        relief="raised",
        borderwidth=2
        )
        self.play_again_button.pack(side=tk.LEFT, padx=5, pady=1)

        # Hent highscore ved oppstart
        self.update_highscores() 
    
    def post_highscore(self, score):
        try:
            data = {"id": GameID, "hs": score, "player": self.player_name}
            print("Sender data til serveren:", data)  # For debugging
            self.resultat = req.post(URL, json=data)  # Send POST-forespørsel

            if self.resultat.status_code == 200:
                print("Highscore sendt!")
                print("Respons:", self.resultat.text)
            
            # Hvis serveren svarer "Updated", hent oppdatert highscore
                if self.resultat.text.strip() == '"Updated"':
                    print("Oppdatering bekreftet. Henter ny highscore...")
                    self.hent_highscore()
            else:
                print("Feil ved sending av highscore. Status:", self.resultat.status_code)
                print("Respons:", self.resultat.text)
        except Exception as e:
            print("Feil ved sending av highscore:", e)
    def hent_highscore(self):
        try:
            response = req.get(URL, params={"id": GameID})
            if response.status_code == 200:
                print("Highscore hentet fra serveren!")
                self.resultat = response  # Lagre responsen for behandling i `update_highscores`
                self.update_highscores()
            else:
                print("Feil ved henting av highscore. Status:", response.status_code)
        except Exception as e:
            print("Feil ved henting av highscore:", e)




    def update_highscores(self):
        try:
            if not self.resultat:  # Sjekk om `self.resultat` er None
                print("Ingen data fra serveren ennå. Ingen highscore å oppdatere.")
                return

            print("Serverrespons tekst:", self.resultat.text)
            print("Serverrespons statuskode:", self.resultat.status_code)

        # Forsøk å tolke JSON manuelt
            import json
            try:
                data = self.resultat.json()  # Håndter JSON-data
            except ValueError:
                print("Feil: Kunne ikke parse JSON. Forsøker manuell parsing...")
                data = json.loads(self.resultat.text)

        # Sjekk om dataen inneholder highscore-liste
            if "highscores" in data:
                highscores = data["highscores"]
            elif "player" in data and "hs" in data:
            # Hvis kun én spiller returneres
                highscores = [{"player": data["player"], "hs": data["hs"]}]
            else:
                print("Ingen highscore-data tilgjengelig.")
                return

        # Rens tidligere highscore-liste
            for widget in self.hs_list.winfo_children():
                widget.destroy()

        # Vis topp 5 eller tilgjengelig data
            for i, entry in enumerate(highscores[:5]):
                hs_label = tk.Label(self.hs_list, text=f"{i+1}. {entry['player']} - {entry['hs']} poeng")
                hs_label.pack(anchor="w")

        except ValueError as e:
            print("Klarte ikke å tolke JSON fra serveren:", e)
            if self.resultat:
                print("Rådata:", self.resultat.text)
        except Exception as e:
            print("Feil ved oppdatering av highscore:", e)

    
    def add_colour(self, colour):
        if len(self.guess) < 4:
            self.guess.append(colour)
            
            # Velg riktig knappetype og størrelse
            if isMac:
                button_class = MacButton
                width, height = 50, 50
            else:
                button_class = tk.Button
                width, height = 5, 2

            # Opprett en knapp for den valgte fargen
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

    def remove_colour(self, button, colour):
        # Fjern knappen fra GUI
        button.destroy()
        # Fjern fargen fra gjetningslisten
        if colour in self.guess:
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
            self.result_label.config(text=f"Gratulerer, {self.player_name}! Du gjettet riktig!")
            self.check_button.config(state=tk.DISABLED)
            self.post_highscore(self.guess_count)
        else:
            self.guess_count += 1
            if self.guess_count >= number_attempts:
                self.result_label.config(
                    text=f"Beklager, du har brukt opp alle forsøkene. Koden var: {secret_code}"
                )
                self.check_button.config(state=tk.DISABLED)
                self.post_highscore(self.guess_count)
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
    def reset_game(self):
        global secret_code
        # Generer en ny hemmelig kode
        secret_code = [random.choice(COLOURS) for _ in range(4)]

        # Nullstill variabler
        self.guess_count = 0
        self.guess = []

        # Fjern alle valgte fargeknapper
        for button in self.chosen_colour_button:
            button.destroy()
        self.chosen_colour_button.clear()

        # Fjern all historikk
        for widget in self.hist_list.winfo_children():
            widget.destroy()

        # Nullstill resultatetiketten
        self.result_label.config(text="")

        # Aktiver "Sjekk Gjetning"-knappen
        self.check_button.config(state=tk.NORMAL)
        self.update_highscores()
    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            self.result_label.config(text="Skriv inn et gyldig navn for å starte!")
        else:
            self.result_label.config(text=f"Lykke til, {self.player_name}!")
            self.name_entry.config(state=tk.DISABLED)
            self.start_button.config(state=tk.DISABLED)
            self.update_highscores()




# Start spillet
root = tk.Tk()
app = Mastermindgame(root)
root.mainloop()
