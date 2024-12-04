import matplotlib.pyplot as plt
from api import getResults

def plot_results():
    try:
        results = getResults()

        forsøk = [int(result["svar"]) for result in results]  
        antall = [int(result["antall"]) for result in results]

        y_min = 0
        y_max = 20
        plt.bar(forsøk, antall, color='red')

<<<<<<< HEAD
    # Lag enkel stolpediagram
    plt.bar(forsøk, antall, color='red')
    plt.xlabel("Antall Forsøk")
    plt.ylabel("Antall Spillere")
    plt.title("Antall forsøk brukt av spillere")
    plt.show()
=======
        plt.ylim(y_min, y_max)

        # Legg til tall over søylene for bedre lesbarhet
        for i, v in enumerate(antall):
            plt.text(forsøk[i], v + 1, str(v), ha='center', va='bottom', fontsize=10)

        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # x aksen tilpasses etter forsøk
        plt.xticks(forsøk)

        plt.xlabel("Antall gjetninger")
        plt.ylabel("Antall ganger greid")
        plt.title("Hvor mange forsøk bruker spillerne?")

        plt.show()

    except Exception as e:
        print(f"Feil i plot_results: {e}")
>>>>>>> cbb6ffb785245dd949a3aebe39c47fc83702e03c
