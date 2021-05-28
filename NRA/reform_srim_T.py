import os.path
import re

# this function reforms transmission SRIM output to a more convenient form
def reform_T(save_path, name_in, name_out):
    
    complete_name_in = os.path.join(save_path, name_in + ".txt") 
    complete_name_out = os.path.join(save_path, name_out + ".txt") 
    fin = open(complete_name_in, "r")
    fout = open(complete_name_out, "w")

    start_data = False
    for line in fin:
        if start_data:
            fout.write(re.sub(',', '.', re.sub('\s+', ' ', re.sub('E', 'e', re.sub('T', 'T ' ,line)))) + "\n")
        elif line.startswith(" Numb"):
            start_data = True

    print("reformed SRIM file with: T ion atom E xyz dir(xyz)")
    fin.close()
    fout.close()
    

save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Full_numerical/'
name_in = "New/transmission_Po_alpha_60realbeam"
name_out = "easyread/easyread_Po_alpha_60realbeam"

reform_T(save_path, name_in, name_out)
