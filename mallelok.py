import tkinter as tk
import random
import requests as req
from tkinter import simpledialog

# Tilgjengelige farger for spillet
farger = ["red", "blue", "green", "yellow", "orange", "purple"]

# Generer en hemmelig kode
hemmelig_kode = [random.choice(farger) for _ in range(4)]
antall_forsøk = 10

# API-opplysninger for highscore
URL = "https://rasmusweb.no/hs.php"
GameID = "Indunu-nomama-wakho"

# Funksjoner for highscore-håndtering
def getHS():
    try:
        resultat = req.get(URL + "?id=" + GameID)
        if resultat.status_code == 200:
            data = resultat.json()
            return int(data.get("hs", float("inf"))), data.get("player", "Ukjent")
    except Exception as e:
        print(f"Feil ved henting av highscore: {e}")
    return float("inf"), "Ukjent"

def postHS(hs, player):
    try:
        data = {"id": GameID, "hs": hs, "player": player}
        req.post(URL, json=data)
    except Exception as e:
        print(f"Feil ved sending av highscore: {e}")

# Mastermind-spillet
class MastermindSpill:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")

        # Spør om spillerens navn
        self.spiller_navn = simpledialog.askstring("Spillerens navn", "Skriv inn navnet ditt:")
        if not self.spiller_navn:
            self.spiller_navn = "Ukjent"

        # Hent eksisterende highscore
        self.current_hs, self.current_player = getHS()
        if self.current_hs is None:
            self.current_hs = float("inf")

        # Initialisering av variabler
        self.gjett_count = 0
        self.gjett = []
        self.valgte_farger_knapper = []

        # Highscore-ramme
        self.highscore_ramme = tk.Frame(root, borderwidth=2, relief="solid", padx=10, pady=10)
        self.highscore_ramme.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.highscore_label = tk.Label(
            self.highscore_ramme, 
            text=f"Highscore:\n{self.current_hs} av {self.current_player}",
            font=("Helvetica", 12, "bold"), 
            fg="blue"
        )
        self.highscore_label.pack()

        # Historikk-ramme
        self.hist_ramme = tk.Frame(root)
        self.hist_ramme.pack(side=tk.TOP, pady=10)

        self.hist_label = tk.Label(self.hist_ramme, text="Tidligere forsøk:", font=("Helvetica", 12, "bold italic"), fg="black", padx=9, pady=3)
        self.hist_label.pack()

        self.hist_liste = tk.Frame(self.hist_ramme)
        self.hist_liste.pack()

        # Instruksjoner
        self.instruksjon = tk.Label(
            root, 
            text="Velg fire farger og trykk på sjekk gjetning", 
            font=("Helvetica", 12, "bold"), 
            fg="black", 
            padx=7, 
            pady=3
        )
        self.instruksjon.pack(pady=10)

        # Fargevalgsknapper
        self.fargeknapper_frame = tk.Frame(root)
        self.fargeknapper_frame.pack()

        for farge in farger:
            knapp = tk.Button(
                self.fargeknapper_frame, 
                bg=farge, 
                width=5, 
                height=2, 
                relief="solid", 
                borderwidth=1, 
                command=lambda f=farge: self.legg_til_farge(f)
            )
            knapp.pack(side=tk.LEFT, padx=5)

        # Valgte farger
        self.valgt_farger_frame = tk.Frame(root)
        self.valgt_farger_frame.pack(pady=10)

        # Kontrollknapper
        self.kontroll_frame = tk.Frame(root)
        self.kontroll_frame.pack()

        self.sjekk_knapp = tk.Button(
            self.kontroll_frame, 
            text="Sjekk Gjetning", 
            command=self.sjekk_gjetning, 
            font=("Helvetica", 12, "bold"), 
            bg="light gray", 
            fg="black", 
            width=10, 
            height=2, 
            relief="raised", 
            borderwidth=2
        )
        self.sjekk_knapp.pack(side=tk.LEFT, padx=5, pady=1)

        self.resultat_label = tk.Label(
            root, 
            text="", 
            font=("Helvetica", 12, "bold"), 
            fg="red"
        )
        self.resultat_label.pack(pady=10)

    def legg_til_farge(self, farge):
        if len(self.gjett) < 4:
            self.gjett.append(farge)
            farge_knapp = tk.Button(
                self.valgt_farger_frame, 
                bg=farge, 
                width=5, 
                height=2, 
                command=lambda fb=farge_knapp, f=farge: self.fjern_farge(fb, f)
            )
            farge_knapp.pack(side=tk.LEFT, padx=5)
            self.valgte_farger_knapper.append(farge_knapp)

    def fjern_farge(self, knapp, farge):
        knapp.destroy()
        self.gjett.remove(farge)

    def sjekk_gjetning(self):
        if len(self.gjett) != 4:
            self.resultat_label.config(text="Velg fire farger før du sjekker.")
            return

        riktig_plassering = sum(1 for i in range(4) if self.gjett[i] == hemmelig_kode[i])
        riktig_farge = sum(min(self.gjett.count(f), hemmelig_kode.count(f)) for f in set(self.gjett)) - riktig_plassering

        self.legg_til_i_historikk(self.gjett, riktig_plassering, riktig_farge)

        if riktig_plassering == 4:
            self.resultat_label.config(text="Gratulerer! Du gjettet koden riktig!")
            self.sjekk_knapp.config(state=tk.DISABLED)
            self.sjekk_highscore()
        else:
            self.gjett_count += 1
            if self.gjett_count >= antall_forsøk:
                self.resultat_label.config(text=f"Beklager, du har brukt opp alle forsøkene. Koden var: {hemmelig_kode}")
                self.sjekk_knapp.config(state=tk.DISABLED)
                self.sjekk_highscore()
            else:
                self.gjett = []
                for knapp in self.valgte_farger_knapper:
                    knapp.destroy()
                self.valgte_farger_knapper.clear()

    def legg_til_i_historikk(self, gjett, riktig_plassering, riktig_farge):
        gjett_ramme = tk.Frame(self.hist_liste)
        gjett_ramme.pack(pady=2, fill=tk.X)

        riktig_farge_label = tk.Label(gjett_ramme, text=f"Riktig farge: {riktig_farge}", font=("Helvetica", 10, "bold"), fg="green")
        riktig_farge_label.pack(side=tk.LEFT, padx=10)

        fargeboks_ramme = tk.Frame(gjett_ramme)
        fargeboks_ramme.pack(side=tk.LEFT, expand=True)

        for farge in gjett:
            farge_boks = tk.Label(fargeboks_ramme, bg=farge, width=2, height=1, relief="solid", borderwidth=1)
            farge_boks.pack(side=tk.LEFT, padx=3)

        riktig_plassering_label = tk.Label(gjett_ramme, text=f"Riktig plassering: {riktig_plassering}", font=("Helvetica", 10, "bold"), fg="blue")
        riktig_plassering_label.pack(side=tk.RIGHT, padx=10)

    def sjekk_highscore(self):
        if self.gjett_count < self.current_hs:
            postHS(self.gjett_count, self.spiller_navn)
            self.resultat_label.config(text=f"Ny highscore! Gratulerer, {self.spiller_navn}!")
            self.highscore_label.config(text=f"Highscore:\n{self.gjett_count} av {self.spiller_navn}")

# Start spillet
root = tk.Tk()
app = MastermindSpill(root)
root.mainloop()
