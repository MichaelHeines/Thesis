#import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import os
import os.path
from lmfit.models import ExpressionModel

# Function that reads all data files in a folder and performs a fit with scaling initial parameters

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
    chan_lim = [round(chan_peak_0 - half_width), round(chan_peak_0 + half_width)]           # sets the region were the peak is fitted
    channel = reader[0][chan_lim[0]:chan_lim[1]]                    # gets a channel list within the region
    counts = reader[2][chan_lim[0]:chan_lim[1]]                     # gets a count list within the region
    chan_peak = np.argmax(counts) + channel[0]                      # reestimates the peak location
    
    fit = gmod.fit(counts, x = channel, amp = max(counts), mu = chan_peak, sigma = half_width/10, a = 100, b = 0.1)         # fits the peak to a gaussian + linear background
    
    try:                                                            # excecutes if the fit is good
        A_max = fit.params['amp'].value
        sigma = fit.params['sigma'].value
        A_exp = math.sqrt(2 * math.pi) * abs(sigma) * A_max         # counts from gaussian integral
        countrate = A_exp/time
        error = np.sqrt(2 * np.pi) * sigma*A_max*((fit.params['sigma'].stderr/sigma) + (fit.params['amp'].stderr/A_max))/time # error on the countrate
        
        #if E == 218.12:
        #    plt.plot(channel, counts)
        #    plt.plot(channel, fit.init_fit, 'k--', label='initial fit')
        
        
        if fit.params['sigma'].stderr/abs(sigma)>0.2:               # extra failsafe for if the fit is bad
            raise ValueError('errors too large')
        return [foil, date, time, index, countrate, error]          # output countrate and the error on the countrate (absolute)
    except:
        print("Fit not sufficient for " + filename + " " + str(E) + " keV peak")
        return 0

main_path = '/mnt/ksf9/H2/user/r0795801/_IO/MEDICIS/MED024_2020/Nov/Pb_castle/raw_data/'
#main_path = 'C:/Users/micha/Documents/school/Master 2e jaar/Masterproef/Data_analysis/Lead Castle/'
save_folder = 'Data/'
save_path = main_path + save_folder

print("trying to make a list of files")
file_list = []
for filename in os.listdir(save_path):                              # appends all files in directory to a list
    f = os.path.join(save_path, filename)
    file_list.append(f)

print("made list of files")

output_file = 'output.txt'                                          # file in which datapoints are collected
f = open(os.path.join(main_path, output_file),"w")
f.write("Foil" + "\t" + "Date" + "\t" + "time" + "\t" + "index" + "\t" + "counts 218" + "\t" + "error 218" + "counts 440" + "\t" + "error 440" + "\n")

gmod = ExpressionModel("amp * exp(-((x - mu)/sigma)**2 / 2) + a - b*x")     # linear + gaussian fitting model

print("wrote first line")

for file in file_list:
    if file.endswith('.csv'):
        complete_name = os.path.join(save_path, file)
        reader = np.array(pd.read_csv(complete_name, header = 1, sep = ";")).T      # load and transpose the csv
        
        counts1 = fit_peak(218.12, 50, reader, gmod, complete_name)
        counts2 = fit_peak(440, 50, reader, gmod, complete_name)
        
        if counts1 == 0:
            f.write(file + "\t" + "ERROR" + "\n")
        else:
            f.write(counts1[0] + "\t" + counts1[1] + "\t" + str(counts1[2]) + "\t" + counts1[3] + "\t" + str(counts1[4]) + "\t" + str(counts1[5]) + "\t" + str(counts2[4]) + "\t" + str(counts2[5]) + "\n")


f.close()
print("Wrote output file")