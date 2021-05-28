import math
import numpy as np
import matplotlib.pyplot as plt
import os.path
import pandas as pd

# Function that compares NRA model to semi-analytic circular model

r_det = math.sqrt(300/math.pi) #* 10**7

save_path_semianalytic = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/Final results/'
name_of_file_semi = 'Circular_60kev_Ac'
semi_name = os.path.join(save_path_semianalytic, name_of_file_semi + ".txt") 
reader_semi = np.array(pd.read_csv(semi_name, header = 1, sep = "\t")).T
r_semi = reader_semi[0]/r_det
eps_semi = reader_semi[1]

save_path_fullnumerical = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Full_numerical/'
name_of_file_full = 'e_geo_numerical_Ac'
full_name = os.path.join(save_path_fullnumerical, name_of_file_full + ".txt")
reader_full = np.array(pd.read_csv(full_name, header = 1, sep = "\t")).T
r_full = reader_full[1]
eps_full = reader_full[2]


#plt.plot(r_semi, eps_semi, label = 'Circular')
#plt.plot(r_full, eps_full, label = 'NRA')
plt.plot(r_semi, (eps_full - eps_semi)/eps_full)
plt.grid()
plt.legend(loc = 'best')
plt.xticks(np.linspace(0, 2, 5), size = 16)
plt.yticks(size = 16)
plt.xlabel("r/rd", fontsize = 16)
plt.ylabel('$\Delta \epsilon/\epsilon$', fontsize = 16)
#plt.ylabel("$\Delta \epsilon$", fontsize = 16)
plt.show()





