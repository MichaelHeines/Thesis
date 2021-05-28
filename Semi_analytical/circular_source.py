import math
import matplotlib.pyplot as plt
import numpy as np
import os.path
import random
import scipy.special as special
import os

os.path.dirname(os.path.abspath(__file__))                      # set directory to that of the python file

def integrand(k, rs, rd):                                       # using an exponential sampling
    bessel1 = k*rs  
    bessel2 = k*rd
    f = special.j1(bessel1) * special.j1(bessel2)/k
    return f

    
def mc_integral(n1, z, rs, rd):                                 # using monte carlo integration to obtain integral
    I = 0                                           
    
    if z/rd < 0.5:                                              # more integrals for small distances
        n = 10 * n1
    elif z/rd < 0.05:
        n = 100 * n1
    else:
        n = n1
    
    for i in range(n):         
        r_num = random.expovariate(z)
        I += (1/n) * (1/z) * (integrand(r_num, rs, rd))         # adding factor, normalized to the exponential distribution
    return I


def circular_source(rs, rd, n1, nr_points, z_min, z_max, save_path, name_of_file):
    prefactor = rd/rs
    z = np.linspace(z_min, z_max, nr_points)                    # values for which the integral is calculated
    circular = []

    for i in z:
        e_geo1 = prefactor * mc_integral(n1, i, rs, rd)
        circular.append(e_geo1)
        print("circular " + str(i/z_max))

    point = []
    for i in z:                                                 # Point source approximation
        e_geo2 = 0.5 - (0.5 * i)/(math.sqrt(rd**2 + i **2))
        point.append(e_geo2)
        

    completeName = os.path.join(save_path, name_of_file+".txt")     # Write a file with the results
    f= open(completeName,"w+")
    f.write("z" + "\t" + "e_circ" + "\t" + "e_point" + "\n")
    for i in range(nr_points):
        f.write(str(z[i]) + "\t" + str(circular[i]) + "\t" + str(point[i]) + "\n")
    f.close()
    print("data file " + name_of_file + " created with: z \t e_circ \t e_point")
    
    plt.plot(z, circular)                               # the circular source efficiency as a function of distance between d and s
    plt.plot(z, point)                                  # point source approximation as a function of distance between d and s


# Running the program for specific parameters
rd = math.sqrt(300/math.pi)                             # absolute detector radius
rs1 = 2.34904313690031
n1 = 10 ** 2                                            # amount of random points for the integral above 0.5
nr_points = 100
z_min = 10**(-2)
z_max = 20
#save_path = "C:/Users/micha/Documents/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/"

file_name1 = "Circular_60kev_locationtest"
save_path = ''

circular_source(rs1, rd, n1, nr_points, z_min, z_max, save_path, file_name1)



"""
nr_points = 100
z_min = 10**-2
z_max = 20

save_path = "C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/"
file_name1 = "circular1.txt"
file_name2 = "circular2.txt"
file_name3 = "circular3.txt"
# z is the distance between the source and the detector

circular_source(rs1, rd, n1, nr_points, z_min, z_max, save_path, file_name1)
circular_source(rs2, rd, n1, nr_points, z_min, z_max, save_path, file_name2)
circular_source(rs3, rd, n1, nr_points, z_min, z_max, save_path, file_name3)

point = []
z = np.linspace(z_min, z_max, nr_points)
for i in z:
    e_geo2 = 0.5 - (0.5 * i)/(math.sqrt(rd**2 + i **2))
    point.append(e_geo2)
plt.plot(z, point)
plt.grid()
plt.legend(["rs = 0.5 rd", "rs = rd", "rs = 2 rd", "point source"])
plt.show()
"""
