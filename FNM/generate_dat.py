import csv
import math
import numpy as np
import os.path

# Program that uses reformed SRIM files to generate appropriate .dat files for the FNM

save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Hard_numerical/'
file_name_in = 'easyread/easyread_Bi_recoil'
file_name_out_p1 = 'dat_out/output_Po_alpha'
file_name_out_p2 = 'dat_out/NA'#'dat_out/output_Pb_recoil_realbeam60'
atomic_number_p1 = "2"
atomic_number_p2 = "82" #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mfraction = 4/209       #Ac225 - Fr221 - At217 - Bi213 - Tl209 - Pb209
sample_width = 10**8
r_det = math.sqrt(300/math.pi) * 10**7
a_energy = 8.5361 * 10**6
# Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
substrate_depth = 5 * 10**3 + 25*10**5            # only for first implantation to turn sample

def generate_toptext(string_alpha, string_recoil):
    line1 = "=========== TRIM with various Incident Ion Energies/Angles and Depths ========= \n"
    line2 = "= This file tabulates the kinetics of incident ions or atoms.                 = \n"
    line3 = "= Col.#1: Ion Number, Col.#2: Z of atom leaving, Col.#3: Atom energy (eV).    = \n"
    line4 = "= Col.#4-6: Last location:  Col.#4: X= Depth into target.                     = \n"
    line5 = "= Col.#7-9: Cosines of final trajectory.                                      = \n"
    line6 = "================ Typical Data File is shown below  ============================ \n"
    line7_1 = string_alpha
    line7_2 = string_recoil
    line8 = "Event  Atom  Energy  Depth   Lateral-Position   ----- Atom Direction ---- \n"
    line9 = "Name   Numb   (eV)    _X_(A)   _Y_(A)  _Z_(A)   Cos(X)   Cos(Y)   Cos(Z) \n"
    line10 = "\n"

    text_alpha = line1+line2+line3+line4+line5+line6+line7_1+line8+line9+line10
    text_recoil = line1+line2+line3+line4+line5+line6+line7_2+line8+line9+line10
    
    return [text_alpha, text_recoil]


def srim_out_to_in(a_energy, atomic_number_p1, atomic_number_p2, mfraction, sample_width, save_path, file_name_in, file_name_out_p1, file_name_out_p2):
    ion_number = []
    x = []
    y = []
    z = []
    complete_name_in = os.path.join(save_path, file_name_in + ".txt")
    complete_name_out_p1 = os.path.join(save_path, file_name_out_p1 + ".txt")
    complete_name_out_p2 = os.path.join(save_path, file_name_out_p2 + ".txt")
    
    with open(complete_name_in, 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        
        for row in reader:
            if float(row[1]) <= (2500000 + 5000):       #in substrate
                if -sample_width <float(row[2])<sample_width and -sample_width<float(row[3])< sample_width:
                    ion = row[0].lstrip("0")
                    while len(ion) < 5:
                        ion = "0" + ion
                    ion_number.append(ion)
                    x.append(abs(float(row[1])))     # for first one -substrate_depth
                    y.append(float(row[2]))
                    z.append(float(row[3]))
                    
            elif float(row[1]) >= (2500000 + 5000 + 202850000):     #in detector
                if float(row[2])**2 + float(row[3])**2 <= r_det**2:
                    ion = row[0].lstrip("0")
                    while len(ion) < 5:
                        ion = "0" + ion
                    ion_number.append(ion)
                    x.append(abs(float(row[1])))     # for first one -substrate_depth
                    y.append(float(row[2]))
                    z.append(float(row[3]))

    N = len(ion_number)
    phi = np.random.uniform(0, 2 * math.pi, N)
    theta = np.arccos(1 - 2 * np.random.random(N))
    energy_p1 = [a_energy]*N
    vec_x = np.cos(phi) * np.sin(theta)
    vec_y = np.sin(phi) * np.sin(theta)
    vec_z = np.cos(theta)
    
    g = open(complete_name_out_p1, 'w')
    h = open(complete_name_out_p2, 'w')
    
    text = generate_toptext("alpha particles", "recoiling particles")
    g.write(text[0])
    h.write(text[1])
    
    for i in range(N):   
        line_p1 = ion_number[i] + "\t" + atomic_number_p1 + "\t" + str("{:e}".format(energy_p1[i])) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(vec_x[i]) + "\t" + str(vec_y[i]) + "\t" + str(vec_z[i]) + "\n"
        line_p2 = ion_number[i] + "\t" + atomic_number_p2 + "\t" + str("{:e}".format(energy_p1[i] * mfraction)) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(- vec_x[i]) + "\t" + str(- vec_y[i]) + "\t" + str(- vec_z[i]) + "\n"
        g.write(line_p1)
        h.write(line_p2)

srim_out_to_in(a_energy, atomic_number_p1, atomic_number_p2, mfraction, sample_width, save_path, file_name_in, file_name_out_p1, file_name_out_p2)
