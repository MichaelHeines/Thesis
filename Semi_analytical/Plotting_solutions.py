import csv
import matplotlib.pyplot as plt
import math
import os.path
import numpy as np

def plot_data(save_path, name_circ, name_gauss):
    complete_circ = os.path.join(save_path, name_circ + ".txt") 
    complete_gauss = os.path.join(save_path, name_gauss + ".txt") 
    z = []
    e_circ = []
    e_gauss = []
    e_point = []

    with open(complete_circ, 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        start_data = False
        for row in reader:
            if start_data:
                z.append(float(row[0])/rd)
                e_circ.append(float(row[1]))
                e_point.append(float(row[2]))
            else:
                start_data = True
                
    with open(complete_gauss, 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        start_data = False
        for row in reader:
            if start_data:
                e_gauss.append(float(row[1]))
            else:
                start_data = True
    
    diff_circ = []
    diff_gauss = []
    for i in range(len(z)):
        diff_circ.append(100*(e_circ[i] - e_point[i])/e_point[i])
        diff_gauss.append(100*(e_gauss[i] - e_point[i])/e_point[i])
    
    print((e_circ[-1] - e_point[-1])/e_point[-1])
    plt.plot(z, diff_circ)
    plt.plot(z, diff_gauss)
    #plt.plot(z, e_point)
    plt.legend(["circle", "gaussian"])
    
    return [z, e_point]
    #plt.plot(z, e_gauss)
    #plt.plot(z, e_point)
    #plt.grid()
z = np.linspace(10**-2, 20, 100)
rd =  math.sqrt(300/math.pi)
save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/Final results/'
name_circ = "Circular_60kev_Ac"
name_gauss = "Gaussian_60kev_Ac"
plot_data(save_path, name_circ, name_gauss)


plt.xticks(size = 16)
plt.yticks(size = 16)
plt.xlabel("r/rd", fontsize = 16)
#plt.ylabel("ε - $ε_{ps}$ (%)", fontsize = 16)
plt.ylabel("Relative difference (%)", fontsize = 16)
plt.grid()
plt.show()

ps_17 = 1/2 * (1 - 17/(math.sqrt(rd**2 + 17**2)))
print(ps_17)