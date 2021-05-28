import csv
import math
import os.path

# Function that recieves the implantation profile and estimates it by a circular Gaussian
def estimate_sd(save_path, name_of_file, col_y, col_z):
    complete_name = os.path.join(save_path, name_of_file + ".txt") 
    y = []
    z = []
    sum1_y = 0
    sum2_y = 0
    sum1_z = 0
    sum2_z = 0

    with open(complete_name, 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        for row in reader:
            y.append(float(row[col_y]) / 10**7)    # y in mm
            z.append(float(row[col_z]) / 10**7)    # z in mm

    for element in y:
        sum1_y += element
        sum2_y += element**2
        
    for element in z:
        sum1_z += element
        sum2_z += element**2
        
    mu_y = sum1_y/len(y)
    mu_z = sum1_z/len(z)
    sigma_y = math.sqrt((sum2_y/len(y)) - mu_y**2)
    sigma_z = math.sqrt((sum2_z/len(z)) - mu_z**2)    
    sigma = math.sqrt((sigma_y**2 + sigma_z**2)/2)
    print("calculated standard deviation")
    print(sigma_y)
    print(sigma_z)
    print(sigma)
    
    return sigma

save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Full_numerical/easyread/'
name_of_file = "easyread_range_Bi_60realbeam"
complete_name = os.path.join(save_path, name_of_file+".txt") 
col_y = 2
col_z = 3


estimate_sd(save_path, name_of_file, col_y, col_z)   
