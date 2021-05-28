import math
import matplotlib.pyplot as plt
import numpy as np
import os.path
import random
import scipy.special as special

def integrand(k, r, rd):
    bessel1 = k*r  
    bessel2 = k*rd
    f = special.j0(bessel1) * special.j1(bessel2) * r
    return f


def mc_int_r(n_r, k, rd, sigma):                    # integration over r
    I_r = 0
    
    for i in range(n_r):
        r = random.normalvariate(0, sigma)          # using normally distributed random numbers
        if r < 0:                                   # making sure r is positive
            r = -r        
        I_r += (1/n_r) * (integrand(k, r, rd))
    return I_r


def mc_int_k(n_k, n_r, z, rd, sigma):               # integration over k
    I_k = 0
    
    if z/rd < 0.1:                                  # more integrals for small distances
        n = 100 * n_k
    elif z/rd < 0.5:
        n = 10 * n_k
    else:
        n = n_k
    
    for i in range(n):
        k = random.expovariate(z)                   # using exponentially distributed random numbers
        I_k += (1/n) * mc_int_r(n_r, k, rd, sigma)
    return I_k


def gaussian_source(sigma, rd, n_r, n_k, nr_points, z_min, z_max, save_path, name_of_file):
    z = np.linspace(z_min, z_max, nr_points)
    gauss = []

    for i in z:
        prefactor = (rd * math.sqrt(math.pi / 2))/(2 * i * sigma) # additional 2 in denominator since r only larger than 0
        e_geo1 = prefactor * mc_int_k(n_k, n_r, i, rd, sigma)
        gauss.append(e_geo1)
        print("gaussian " + str(i/z_max))

    point = []
    for i in z:
        e_geo2 = 0.5 - (0.5 * i)/(math.sqrt(rd**2 + i **2))
        point.append(e_geo2)
    
    completeName = os.path.join(save_path, name_of_file+".txt") 
    f= open(completeName,"w+")
    f.write("z" + "\t" + "e_gauss" + "\t" + "e_point" + "\n")
    for i in range(nr_points):
        f.write(str(z[i]) + "\t" + str(gauss[i]) + "\t" + str(point[i]) +"\n")
    f.close()
    print("data file " + name_of_file + " created with: z \t e_gauss \t e_point")

    plt.plot(z, gauss)                                  # the exact efficiency as a function of distance between d and s
    plt.plot(z, point)                                  # point source approximation

    
# Excecution for specific parameters    
#sigma = 5                                          # standard deviation of the source
rd = math.sqrt(300/math.pi)                         # absolute detector radius
n_r = 10 ** 2                                       # amount of random points for the integral of r, 10^2 is ussualy enough
n_k = 10 ** 4                                       # amount of random points for the integral of k
nr_points = 100                                     # number of distances for the calculation
z_min = 10**-2
z_max = 20
# z is the distance between the source and the detector
sigma = 1.174521568450155

save_path = "C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/"
file_name = "Gaussian_60kev"
print("start")

gaussian_source(sigma, rd, n_r, n_k, nr_points, z_min, z_max, save_path, file_name)


point = []
z = np.linspace(z_min, z_max, nr_points)
for i in z:
    e_geo2 = 0.5 - (0.5 * i)/(math.sqrt(rd**2 + i **2))
    point.append(e_geo2)
plt.plot(z, point)
plt.grid()
plt.legend(["Gaussian", "point source"])
plt.show()

#gaussian_source(sigma, rd, n_r, n_k, nr_points, z_min, z_max)
