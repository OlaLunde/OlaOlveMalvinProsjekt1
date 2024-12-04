from pprint import pprint
import matplotlib.pyplot as plt
from Spill import api
forsøk = []
antall = []

for result in results:
    print(result)
    forsøk.append(result["svar"])
    antall.append(result["antall"])
    
print(forsøk, antall)


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
