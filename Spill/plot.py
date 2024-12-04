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


"""
# verdier = linje.strip().split(":")   # .strip fjærner whitespaces / linjeskift.  split(";") viser at man splitter tallene ved tegnet ;
forsøk.append((verdier[0]))
antall.append(float(verdier[1])) 

plt.barh(forsøk, folk, zorder = 2)
plt.xlim(0, 100)
plt.xticks(rotation = 50, fontsize = 12)
plt.yticks(rotation = 30, fontsize = 8)
plt.grid(zorder = 0)
plt.show()
"""