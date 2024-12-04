import matplotlib.pyplot as plt
from Spill import api
forsøk = []
folk = []

with open("Spill/api.py", encoding ="utf-8") as fil:
    for data in fil:
        verdier = data.strip().split(",")  
        forsøk.append((verdier[0]))
        folk.append(float(verdier[1])) 

plt.barh(forsøk, folk, zorder = 2)
plt.xlim(0, 100)
plt.xticks(rotation = 50, fontsize = 12)
plt.yticks(rotation = 30, fontsize = 8)
plt.grid(zorder = 0)
plt.show()
