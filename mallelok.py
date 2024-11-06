import tkinter as tk
import random

# Tilgjengelige farger for spillet
farger = ["red", "blue", "green", "yellow", "orange", "purple"]

# Generer en hemmelig kode
hemmelig_kode = [random.choice(farger) for _ in range(4)]
antall_forsøk = 10

class MastermindSpill:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")

        # Initialisering
        self.gjett_count = 0
        self.gjett = []
        self.valgte_farger_knapper = []  # Holder knappene for valgte farger
        
        # Ramme for tidligere gjetninger
        self.hist_ramme = tk.Frame(root)
        self.hist_ramme.pack(side=tk.TOP, pady=10)

        # Historikk label
        self.hist_label = tk.Label(self.hist_ramme, text="Tidligere forsøk:", font=("Helvetica", 12, "bold italic"),  # Endrer font, størrelse, og stil
            fg="black", # Endrer bakgrunnsfargen
            padx=9,  # Legger til ekstra plass rundt teksten (horisontalt)
            pady=3,   )
        self.hist_label.pack()

        # Ramme for tidligere forsøk-liste
        self.hist_liste = tk.Frame(self.hist_ramme)
        self.hist_liste.pack()

        # Lag hovedlayouten
        self.instruksjon = tk.Label(root, text="Velg fire farger og trykk på sjekk gjetning", font=("Helvetica", 12, "bold"),  # Endrer font, størrelse, og stil
            fg="black", # Endrer bakgrunnsfargen
            padx=7,  # Legger til ekstra plass rundt teksten (horisontalt)
            pady=3,)
        self.instruksjon.pack(pady=10)

        # Lag en ramme for fargevalg
        self.fargeknapper_frame = tk.Frame(root)
        self.fargeknapper_frame.pack()

        # Opprett fargeknappene
        for farge in farger:
            knapp = tk.Button(self.fargeknapper_frame, bg=farge, width=5, height=2, relief="solid", borderwidth=1,
                              command=lambda f=farge: self.legg_til_farge(f))
            knapp.pack(side=tk.LEFT, padx=5)

        # Ramme for valgte farger
        self.valgt_farger_frame = tk.Frame(root)
        self.valgt_farger_frame.pack(pady=10)

        # Knapperamme for å sjekke gjetning og nullstille
        self.kontroll_frame = tk.Frame(root)
        self.kontroll_frame.pack()

        # Sjekk-knapp med styling
        self.sjekk_knapp = tk.Button(
            self.kontroll_frame,
            text="Sjekk Gjetning",
            command=self.sjekk_gjetning,
            font=("Helvetica", 12, "bold"),  # Større og fet tekst
            bg="light gray",  # Blå bakgrunnsfarge
            fg="black",  # Hvit tekstfarge
            activebackground="white",  # Mørk blå bakgrunn når knappen trykkes
            activeforeground="black",  # Hvit tekst når knappen trykkes
            width=12,  # Økt bredde
            height=2,  # Økt høyde
            relief="raised",  # Tredimensjonal effekt
            borderwidth=2  # Tykkere kant
        )
        self.sjekk_knapp.pack(side=tk.LEFT, padx=5, pady=1)  # Ekstra avstand rundt knappen

        # Tilbakemelding med styling
        self.resultat_label = tk.Label(
            root,
            text="",  # Start med tom tekst
            font=("Helvetica", 12, "bold"),  # Fet tekst
            fg="red",  # Rød tekstfarge
            
        )
        self.resultat_label.pack(pady=10)  # Avstand rundt etiketten

    def legg_til_farge(self, farge):
        # Legg til farge hvis det er plass i gjettningen
        if len(self.gjett) < 4:
            self.gjett.append(farge)
            # Opprett en knapp for den valgte fargen
            # Definer `farge_knapp` før vi bruker den i lambda-funksjonen
            farge_knapp = tk.Button(self.valgt_farger_frame, bg=farge, width=5, height=2)
            farge_knapp.config(command=lambda fb=farge_knapp, f=farge: self.fjern_farge(fb, f))
            farge_knapp.pack(side=tk.LEFT, padx=5)
            self.valgte_farger_knapper.append(farge_knapp)

    def fjern_farge(self, knapp, farge):
        # Fjern valgt farge både fra GUI og fra gjett-listen
        knapp.destroy()
        self.gjett.remove(farge)

    def sjekk_gjetning(self):
        if len(self.gjett) != 4:
            self.resultat_label.config(text="Velg fire farger før du sjekker.")
            return

        # Sjekk korrekt plassering
        riktig_plassering = sum(1 for i in range(4) if self.gjett[i] == hemmelig_kode[i])

        # Sjekk riktige farger, men feil plassering
        riktig_farge = sum(min(self.gjett.count(f), hemmelig_kode.count(f)) for f in set(self.gjett)) - riktig_plassering

        # Legg gjetningen til i historikken
        self.legg_til_i_historikk(self.gjett, riktig_plassering, riktig_farge)

        # Vinn eller taper melding
        if riktig_plassering == 4:
            self.resultat_label.config(text="Gratulerer! Du gjettet koden riktig!")
            self.sjekk_knapp.config(state=tk.DISABLED)
        else:
            self.gjett_count += 1
            if self.gjett_count >= antall_forsøk:
                self.resultat_label.config(
                    text=f"Beklager, du har brukt opp alle forsøkene. Koden var: {hemmelig_kode}"
                )
                self.sjekk_knapp.config(state=tk.DISABLED)
            else:
                # Nullstill for ny gjetning
                self.gjett = []
                for knapp in self.valgte_farger_knapper:
                    knapp.destroy()
                self.valgte_farger_knapper.clear()

    def legg_til_i_historikk(self, gjett, riktig_plassering, riktig_farge):
    # Lag en ny ramme for hver gjetning
        gjett_ramme = tk.Frame(self.hist_liste)
        gjett_ramme.pack(pady=2, fill=tk.X)

    # Lag en ramme for "Riktig farge" til venstre
        riktig_farge_ramme = tk.Frame(gjett_ramme)
        riktig_farge_ramme.pack(side=tk.LEFT, padx=10)

    # Etikett for riktig farge (venstre)
        riktig_farge_label = tk.Label(
            riktig_farge_ramme, 
            text=f"Riktig farge: {riktig_farge}", 
            font=("Helvetica", 10, "bold"),
            fg="green"
        )
        riktig_farge_label.pack()

    # Lag en ramme for fargeboksene i midten
        fargeboks_ramme = tk.Frame(gjett_ramme)
        fargeboks_ramme.pack(side=tk.LEFT, expand=True)

    # Vis farger for gjetningen som større bokser
        for farge in gjett:
            farge_boks = tk.Label(fargeboks_ramme, bg=farge, width=2, height=1, relief="solid", borderwidth=1)
            farge_boks.pack(side=tk.LEFT, padx=3)

    # Lag en ramme for "Riktig plassering" til høyre
        riktig_plassering_ramme = tk.Frame(gjett_ramme)
        riktig_plassering_ramme.pack(side=tk.RIGHT, padx=10)

    # Etikett for riktig plassering (høyre)
        riktig_plassering_label = tk.Label(
            riktig_plassering_ramme, 
            text=f"Riktig plassering: {riktig_plassering}", 
            font=("Helvetica", 10, "bold"),
            fg="blue"
        )
        riktig_plassering_label.pack()

    # Legg til en horisontal strek for å skille hver gjetning
        separator = tk.Frame(self.hist_liste, height=1, bd=1, relief="sunken", bg="black")
        separator.pack(fill=tk.X, pady=3)


# Start spillet
root = tk.Tk()
app = MastermindSpill(root)
root.mainloop()
