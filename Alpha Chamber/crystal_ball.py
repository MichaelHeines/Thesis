import numpy as np
import matplotlib.pyplot as plt

a = 1
n = [0.1, 0.5, 1, 100]
x = np.linspace(-30, 30, 100)


for i in range(len(n)): 
    f = np.zeros(len(x))
    
    for j in range(len(x)):
        if (-a < x[j] < a):
            f[j] = np.exp((-x[j]**2)/2)
        elif (-a > x[j]):
            A = (n[i]/a)**n[i] * np.exp(-a**2/2)
            B = n[i]/a - a
            f[j] = A * (B - x[j])**(-n[i])
        else:
            A = (n[i]/a)**n[i] * np.exp(-a**2/2)
            B = n[i]/a - a
            f[j] = A * (B + x[j])**(-n[i])
        
    plt.plot(x, f, label = "n = " + str(n[i]))
    
plt.grid()
plt.legend(loc = 'best')
plt.xlabel(r"$\frac{x-\mu}{\sigma}$", fontsize = 16)
plt.ylabel(r'$\frac{f}{N}$', fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)