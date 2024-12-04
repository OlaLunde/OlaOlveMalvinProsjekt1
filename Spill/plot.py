import matplotlib.pyplot as plt
from api import getResults

def plot_results():
    # Hent data fra API
    results = getResults()

    forsøk = []
    antall = []

    for result in results:
        forsøk.append(result["svar"])
        antall.append(result["antall"])

    # Lag enkel stolpediagram
    plt.bar(forsøk, antall, color='red')
    plt.xlabel("Antall Forsøk")
    plt.ylabel("Antall Spillere")
    plt.title("Antall forsøk brukt av spillere")
    plt.show()