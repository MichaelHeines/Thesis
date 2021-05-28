import csv
import os.path

# Program that transforms separate data files for the different models in a single file for easier use

def total_output(save_path, name_circular, name_gaussian, name_combined):
    complete_name_circular = os.path.join(save_path, name_circular + ".txt") 
    complete_name_gaussian = os.path.join(save_path, name_gaussian + ".txt") 
    complete_name_output = os.path.join(save_path, name_combined + ".txt")
    z = []
    e_circular = []
    e_gaussian = []
    e_point = []
    
    with open(complete_name_circular, 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        start_data = False
        for row in reader:
            if start_data: 
                z.append(float(row[0]))                 # z in mm
                e_circular.append(float(row[1]))
            else:
                start_data = True
            
    with open(complete_name_gaussian, 'r') as g:
        reader = csv.reader(g, delimiter = '\t')
        start_data = False
        for row in reader:
            if start_data:
                e_gaussian.append(float(row[1]))
                e_point.append(float(row[2]))
            else:
                start_data = True
            
        fout = open(complete_name_output, "w")
        fout.write("z \t e_circ \t e_gauss \t e_point \n")
            
    for i in range(len(z)):
        fout.write(str(z[i]) + "\t" + str(e_circular[i]) + "\t" + str(e_gaussian[i]) + "\t" + str(e_point[i]) + "\n")
            
    print("data file " + name_combined + " created with: z \t e_circ \t e_gauss \t e_point")
    
    
#name_circular = "output_circular"                   # name datafile circular
#name_gaussian = "output_gaussian"                   # name datafile gaussian
#name_combined = "output_complete"                   # name complete datafile
#save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/'

#total_output(save_path, name_circular, name_gaussian, name_combined)