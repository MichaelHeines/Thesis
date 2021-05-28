import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import os.path

# Program that checks if the final position of a particle is on the detector to apply the FNM

save_path = 'C:/Users/micha/Documents/school/Master 2e jaar/Masterproef/Data_calculations/Hard_numerical/easyread/'
file_name_alpha = "easyread_Po_alpha"
#file_name_recoil = "easyread_At_recoil"
complete_name_alpha = os.path.join(save_path, file_name_alpha + '.txt')
#complete_name_recoil = os.path.join(save_path, file_name_recoil + '.txt')

N = 0
r_det = math.sqrt(300/math.pi) * 10**7
branching = 1

with open(complete_name_alpha, 'r') as f:       # counts for the primary decay and their energies
    reader = csv.reader(f, delimiter = ' ')
    for row in reader:
        if float(row[1]) >= (2500000 + 5000 + 202850000):     #in detector
            if float(row[2])**2 + float(row[3])**2 <= r_det**2:  
                N += 1

            
print((N*branching/10**3))


            

        
        
