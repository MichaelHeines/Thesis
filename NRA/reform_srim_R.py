import os.path
import re

# this function reforms ion range SRIM output to a more convenient form
def reform_R(save_path, name_in, name_out):
    
    complete_name_in = os.path.join(save_path, name_in + ".txt") 
    complete_name_out = os.path.join(save_path, name_out + ".txt") 
    fin = open(complete_name_in, "r")
    fout = open(complete_name_out, "w")

    start_data = False
    for line in fin:
        if start_data:
            fout.write(re.sub(',', '.', re.sub('\s+', ' ', re.sub('E', 'e', line))) + "\n")
        elif line.startswith("-------"):
            start_data = True

    print("reformed SRIM file with: ion x y z")
    fin.close()
    fout.close()
    

save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Hard_numerical/'
name_in = "range_Po_alpha"
name_out = "easyread/easyread_Po_alpha"

reform_R(save_path, name_in, name_out)