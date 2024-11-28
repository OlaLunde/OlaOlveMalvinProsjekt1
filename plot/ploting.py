import matplotlib.pyplot as plt
from Spill import mastermind

forsok = []
person = []

with open("", encoding ="utf-8") as fil:
    for linje in fil:
        verdier = linje.strip().split(";")   # .strip fjærner whitespaces / linjeskift.  split(";") viser at man splitter tallene ved tegnet ;
        forsok.append((verdier[0]))
        person.append((verdier[1].replace(",", ".")))  # replace bytter ut det første tegnet man skriver med det andre


plt.plot(forsok, person)
#plt.xlim(0, 100)
plt.xticks(rotation = 50, fontsize = 8)
plt.yticks(rotation = 30, fontsize = 8)
#plt.grid()
plt.show()
