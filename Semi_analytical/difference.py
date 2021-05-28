import csv
import matplotlib.pyplot as plt
import math
import os.path

# Load in the generated data
save_path = "C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/"
name_file_c1 = "circular1"
name_file_c2 = "circular2"
name_file_c3 = "circular3"
name_file_g1 = "gaussian1"
name_file_g2 = "gaussian2"
name_file_g3 = "gaussian3"

complete_name_c1 = os.path.join(save_path, name_file_c1 +".txt")
complete_name_c2 = os.path.join(save_path, name_file_c2 +".txt")
complete_name_c3 = os.path.join(save_path, name_file_c3 +".txt")
complete_name_g1 = os.path.join(save_path, name_file_g1 +".txt")
complete_name_g2 = os.path.join(save_path, name_file_g2 +".txt")
complete_name_g3 = os.path.join(save_path, name_file_g3 +".txt")

z = []
c1 = []
c2 = []
c3 = []
g1 = []
g2 = []
g3 = []
diff1 = []
diff2 = []
diff3 = []
rd = math.sqrt(300/math.pi)

with open(complete_name_c1, 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    start_data = False
    for row in reader:
        if start_data:
            z.append(float(row[0])/rd)
            c1.append(float(row[1]))
        else:
            start_data = True
            
with open(complete_name_c2, 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    start_data = False
    for row in reader:
        if start_data:
            c2.append(float(row[1]))
        else:
            start_data = True
            
with open(complete_name_c3, 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    start_data = False
    for row in reader:
        if start_data:
            c3.append(float(row[1]))
        else:
            start_data = True
            
with open(complete_name_g1, 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    start_data = False
    for row in reader:
        if start_data:
            g1.append(float(row[1]))
        else:
            start_data = True
            
with open(complete_name_g2, 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    start_data = False
    for row in reader:
        if start_data:
            g2.append(float(row[1]))
        else:
            start_data = True
            
with open(complete_name_g3, 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    start_data = False
    for row in reader:
        if start_data:
            g3.append(float(row[1]))
        else:
            start_data = True
            
# Get the difference between the models
for i in range(len(z)):
    diff1.append(c1[i] - g1[i])
    diff2.append(c2[i] - g2[i])
    diff3.append(c3[i] - g3[i])
    
# Plot the difference between the models
plt.plot(z, diff1)
plt.plot(z, diff2)
plt.plot(z, diff3)
plt.xticks(size = 16)
plt.yticks(size = 16)
plt.xlabel("r/rd", size = 16)
plt.ylabel("∆ε", size = 16)
plt.legend(["rs = 0.5 rd", "rs = rd", "rs = 2 rd", "point source"], fontsize = 16)
plt.grid()
plt.show()