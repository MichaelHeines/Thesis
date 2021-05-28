import math
import matplotlib.pyplot as plt
import numpy as np

# Program that calculates and plots the theoretical difference between the circular and gaussian models at a distance 0

def function(rs):
    ls = []
    for i in rs:
        if i <= 1:
            point = math.exp(-2/(i**2))/2
        elif i > 1:
            point = (1/(i**2) - 1 + math.exp(-2/(i**2)))/2
        ls.append(point)
    return ls
        
    
rs = np.linspace(10**-2, 10, 1000)
plt.plot(rs, function(rs))
plt.yticks(size = 18)
plt.xticks(np.linspace(0, 10, 11), size = 18)
plt.xlabel("rs/rd", size = 18)
plt.ylabel("∆ε", size = 18)
plt.grid()
plt.show()