import matplotlib.pyplot as plt
forsøk = []
folk = []

with open("api.py", encoding ="utf-8") as fil:
    for linje in fil:
        verdier = linje.strip().split(":")   # .strip fjærner whitespaces / linjeskift.  split(";") viser at man splitter tallene ved tegnet ;
        forsøk.append((verdier[0]))
        folk.append(float(verdier[1])) 

plt.barh(forsøk, folk, zorder = 2)
plt.xlim(0, 100)
plt.xticks(rotation = 50, fontsize = 12)
plt.yticks(rotation = 30, fontsize = 8)
plt.grid(zorder = 0)
plt.show()
