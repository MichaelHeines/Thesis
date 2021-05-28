import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import os
import os.path
from lmfit.models import ExpressionModel

# This function estimates the fraction of Gaussian fit in short and long range, to quantify pile-up

def convert_E (E):                                                  # provides initial energy calibration
    chan = (E - 139.983)/0.61061
    return chan


def fit_peak(E, half_width, reader, gmod, filename):                # fits for filename a peak at energy E, expected to lie within halfwidth of that value, from reader with the fit expression gmod
    name = filename.split('/')[-1].split('.csv')[0].strip('s')      # obtains the name of a file and removes .csv and possibly s
    time = float(name.split('_')[-1])                               # splits the name into different strings and takes the final part to obtain the time
    foil = name.split('_')[2]
    date = name.split('_')[4] + "/" + name.split('_')[3]
    index = name.split('_')[5]
    
    chan_peak_0 = convert_E(E)                                      # sets initial calibration location
    chan_lim_0 = [round(chan_peak_0 - half_width), round(chan_peak_0 + half_width)]           # sets the region were the peak is fitted
    channel = reader[0][chan_lim_0[0]:chan_lim_0[1]]                    # gets a channel list within the region
    counts = reader[2][chan_lim_0[0]:chan_lim_0[1]]                     # gets a count list within the region

    true_peak = int(counts.argmax() + channel[0])
    
    channel_narrow = reader[0][true_peak-4:true_peak+4]
    channel_broad = reader[0][true_peak-10:true_peak+10]
    counts_narrow = reader[2][true_peak-4:true_peak+4]*10**-4
    counts_broad = reader[2][true_peak-10:true_peak+10]*10**-4
  
    fit_narrow = gmod.fit(counts_narrow, x = channel_narrow, amp = max(counts_narrow), mu = true_peak, sigma = 2, a = 100, b = 0.1)         # fits the peak to a gaussian + linear background
    fit_broad = gmod.fit(counts_broad, x = channel_broad, amp = max(counts_broad), mu = true_peak, sigma = 2, a = 100, b = 0.1)
    
    print(fit_broad.fit_report())
    try:                                                                # excecutes if the fit is good
        A_max_n = fit_narrow.params['amp'].value
        sigma_n = fit_narrow.params['sigma'].value
        A_exp_n = math.sqrt(2 * math.pi) * abs(sigma_n) * A_max_n         # counts from gaussian integral
        countrate_n = A_exp_n/time        
        
        A_max = fit_broad.params['amp'].value
        sigma = fit_broad.params['sigma'].value
        A_exp = math.sqrt(2 * math.pi) * abs(sigma) * A_max         # counts from gaussian integral
        countrate = A_exp/time       
        pile_up = countrate_n/countrate
        print(pile_up)

        
        if E == 218.12:
            plt.plot(channel_broad, counts_broad*10**-4, 'o', color = 'black', label = 'data')
            plt.plot(channel_broad, fit_broad.best_fit*10**-4, 'r--', label='best fit')
            
            plt.legend(loc = 'best')
            plt.xticks(size = 12)
            plt.yticks(size = 12)
        
        
        if fit_broad.params['sigma'].stderr/abs(sigma)>0.2:               # extra failsafe for if the fit is bad
            raise ValueError('errors too large')
            
        return [foil, date, time, index, countrate, pile_up]          # output countrate and the error on the countrate (absolute)
        

    except:
        print("Fit not sufficient for " + filename + " " + str(E) + " keV peak")
        return 0

    
# To run on the cluster
"""
main_path = '/mnt/ksf9/H2/user/r0795801/_IO/MEDICIS/MED024_2020/Nov/Pb_castle/raw_data/'
save_folder = 'Data/'
save_path = main_path + save_folder

print("trying to make a list of files")
file_list = []
for filename in os.listdir(save_path):                              # appends all files in directory to a list
    f = os.path.join(save_path, filename)
    file_list.append(f)

print("made list of files")

out_path = '/mnt/ksf9/H2/user/r0795801/share/my.public/Pb_Castle/'
output_file = 'pileup.txt'                                          # file in which datapoints are collected
f = open(os.path.join(out_path, output_file),"w")
f.write("218" + "\t" + "440" + "\n")
print("wrote first line")

gmod = ExpressionModel("amp * exp(-((x - mu)/sigma)**2 / 2) + a - b*x")     # linear + gaussian fitting model


for file in file_list:
    if file.endswith('.csv'):
        complete_name = os.path.join(save_path, file)
        reader = np.array(pd.read_csv(complete_name, header = 1, sep = ";")).T      # load and transpose the csv
        
        counts1 = fit_peak(218.12, 50, reader, gmod, complete_name)
        counts2 = fit_peak(440, 50, reader, gmod, complete_name)
        
        if counts1 == 0:
            f.write(file + "\t" + "ERROR" + "\n")
        else:
            f.write(str(counts1[5]) + "\t" + str(counts2[5]) + "\n")


f.close()
print("Wrote output file")
    
    
    
    
"""
main_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_analysis/Lead Castle/'
save_folder = 'Data/'
save_path = main_path + save_folder

file = 'Ac_225_m108_11_17_post_LN2_11234.8.csv'

gmod = ExpressionModel("amp * exp(-((x - mu)/sigma)**2 / 2) + a - b*x")     # linear + gaussian fitting model

complete_name = os.path.join(save_path, file)
reader = np.array(pd.read_csv(complete_name, header = 1, sep = ";")).T      # load and transpose the csv

counts1 = fit_peak(218.12, 20, reader, gmod, complete_name)
counts2 = fit_peak(440, 20, reader, gmod, complete_name)

print(counts1)
print(counts2)
plt.grid()
plt.xlabel('channel', fontsize = 16)
plt.ylabel('Counts $(10^{4})$', fontsize = 16)
plt.show()
