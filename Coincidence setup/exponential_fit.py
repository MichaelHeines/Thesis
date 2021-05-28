import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math
import numpy as np
import pandas as pd
import os
import os.path
import copy
from lmfit.models import ExpressionModel
from lmfit.models import Model

# This file uses the root output csv files to perform an exponential decay fitting

def mean_time(start_times, len_sec, decay_cte):         # returns mean time in days
    len_days = len_sec/(24*3600)
    mean_times = np.zeros(len(len_days))
    
    for i in range(len(len_days)):
        mean_times[i] = start_times[i] + len_days[i] + (1/decay_cte)*math.log(decay_cte*len_days[i]) - (1/decay_cte)*math.log(np.exp(decay_cte*len_days[i])-1)
        
    return mean_times

def decay(x, N, dec):
    dec = decay_cte
    return N*np.exp(-x * dec)

t_2 = 9.9203                            # half life in days
decay_cte = np.log(2)/t_2                   # decay constant in /days

save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_analysis/Coincidence/'
filename = 'M120_data points_binI_scaledroot.csv'
complete_name = os.path.join(save_path, filename)

reader = np.array(pd.read_csv(complete_name, header = 1, sep = ";")).T             # load in data

unprocessed_index = reader[0]
del_t_init = reader[1]/86400
meas_t = reader[2]
unprocessed_A_Bi = reader[3]#*1.07
unprocessed_A_Bi_err = reader[4]
unprocessed_A_Tl = reader[5]#*1.07
unprocessed_A_Tl_err = reader[6]

index = []
for i in range(len(unprocessed_index)):
    index.append(unprocessed_index[i][-6])                #(unprocessed_index[i].lstrip("M120_"))

"""
# M108: 0, 2, 3, 4, 5, 6, 7, 8
day_0 = 4 #4 and 5 /11 for 108 and 118                               # time of collection
month_0 = 11
time_0 = 11 #+ 40/60 #11:00 and 13:40
day = np.array([14, 18, 19, 22, 26, 2, 11, 22])
month = np.array([11, 11, 11, 11, 11, 12, 12, 13])
hours = np.array([12 + 3/60, 14 + 20/60, 18 + 34/60, 10 + 58/60, 12 + 40/60, 17 + 49/60, 10 + 40/60, 14 + 23/60])
"""
# M120: 1, 2, 3, 4, 5, 6
day_0 = 9
month_0 = 12
time_0 = 15
day = np.array([15, 17, 23, 30, 8, 14])
month = np.array([12, 12, 12, 12, 13, 13])
hours = np.array([15 + 30/60, 16 + 24/60, 9 + 28/60, 14 + 14/60, 14 + 41/60, 14 + 41/60])


time_start_aquisition = 30*(month-month_0) + (day-day_0) + (hours-time_0)/24
time_initial = np.zeros(len(index))
len_files = np.exp(- decay_cte * time_start_aquisition)
#print(len_files/len_files[0])

for i in range(len(index)):
    if (index[i] == "1") or (index[i] == "0"):
        time_initial[i] = time_start_aquisition[0] + del_t_init[i]
    elif index[i] == "2":
        time_initial[i] = time_start_aquisition[1] + del_t_init[i]
    elif index[i] == "3":
        time_initial[i] = time_start_aquisition[2] + del_t_init[i]
    elif index[i] == "4":
        time_initial[i] = time_start_aquisition[3] + del_t_init[i]
    elif index[i] == "5":
        time_initial[i] = time_start_aquisition[4] + del_t_init[i]
    elif index[i] == "6":
        time_initial[i] = time_start_aquisition[5] + del_t_init[i]
    elif index[i] == "7":
        time_initial[i] = time_start_aquisition[6] + del_t_init[i]
    elif index[i] == "8":
        time_initial[i] = time_start_aquisition[7] + del_t_init[i]
        
mean_times = mean_time(time_initial, meas_t, decay_cte)

A_Bi = np.zeros(len(unprocessed_A_Bi))
A_Bi_err = np.zeros(len(unprocessed_A_Bi))
A_Tl = np.zeros(len(unprocessed_A_Bi))
A_Tl_err = np.zeros(len(unprocessed_A_Bi))
for i in range(len(A_Bi)):
    A_Bi[i] = unprocessed_A_Bi[i]
    A_Tl[i] = unprocessed_A_Tl[i]
    A_Bi_err[i] = unprocessed_A_Bi_err[i]
    A_Tl_err[i] = unprocessed_A_Tl_err[i]


begin = 0
end = len(mean_times)-1
mean_times = mean_times[begin:end]
A_Bi = A_Bi[begin:end]
A_Bi_err = A_Bi_err[begin:end]
A_Tl = A_Tl[begin:end]
A_Tl_err = A_Tl_err[begin:end]

t_cont = np.linspace(0, mean_times[-1], 100)
errorbars_Bi = A_Bi * A_Bi_err
errorbars_Tl = A_Tl * A_Tl_err

"""
gmod = ExpressionModel("N * exp(-dec*x)")
fit_Bi = gmod.fit(A_Bi, x = mean_times, N = 10**3, dec = decay_cte,  weights = 1/errorbars_Bi)
fit_Tl = gmod.fit(A_Tl, x = mean_times, N = 10**3, dec = decay_cte, weights = 1/errorbars_Tl)
"""
gmod = ExpressionModel("N * exp(-0.0698715946654784*x)")
fit_Bi = gmod.fit(A_Bi, x = mean_times, N = 10**3, weights = 1/errorbars_Bi)
fit_Tl = gmod.fit(A_Tl, x = mean_times, N = 10**3, weights = 1/errorbars_Tl)


print(fit_Bi.fit_report())
print(fit_Tl.fit_report())

N_Bi = fit_Bi.params['N'].value
N_Tl = fit_Tl.params['N'].value
N_Bi_err = fit_Bi.params['N'].stderr
N_Tl_err = fit_Tl.params['N'].stderr
"""
lambda_Bi = fit_Bi.params['dec'].value
lambda_Tl = fit_Tl.params['dec'].value
lambda_Bi_err = fit_Bi.params['dec'].stderr
lambda_Tl_err = fit_Tl.params['dec'].stderr
"""
lambda_Bi = decay_cte
lambda_Tl = decay_cte

err_Bi = np.sqrt((N_Bi_err/N_Bi)**2 + (14/173)**2 + (0.1/97.8)**2 + (20/100355)**2)
err_Tl = np.sqrt((N_Tl_err/N_Tl)**2 + (0.02/1)**2 + (0.1/2.2)**2 + (33/100370)**2)
print(str(N_Bi) + " +/- " + str(err_Bi*100) + "%")
print(str(N_Tl) + " +/- " + str(err_Tl*100) + "%")

resulting_fit_Bi = N_Bi * np.exp(- t_cont * lambda_Bi)
resulting_fit_Tl = N_Tl * np.exp(- t_cont * lambda_Tl)


# Activities
plt.plot(t_cont, resulting_fit_Bi, 'r', label = 'Bi coincidences')
plt.plot(t_cont, resulting_fit_Tl, 'b--', label = 'Tl coincidences')
plt.plot(mean_times, A_Bi, 'rv', markersize = 4)
plt.errorbar(mean_times, A_Bi, yerr=errorbars_Bi, fmt='none', ecolor = 'red')
plt.plot(mean_times, A_Tl, 'bo', markersize = 4)
plt.errorbar(mean_times, A_Tl, yerr=errorbars_Tl, fmt='none', ecolor = 'blue')

plt.xlabel("Time since EOC (days)", fontsize = 16)
plt.ylabel("Activity (kBq)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
Bi_line = mlines.Line2D([], [], color='red', marker='v', markersize = 4, linestyle = '-', label='Bi coincidences')
Tl_line = mlines.Line2D([], [], color = 'Blue', marker='o', markersize = 4, linestyle = '--', label='Tl coincidences')
plt.legend(handles=[Bi_line, Tl_line])
plt.grid()
plt.show()
"""

# Residues
diff_Bi = []
diff_Tl = []
for i in range(len(mean_times)):
    diff_Bi.append((A_Bi[i]-fit_Bi.best_fit[i]))
    diff_Tl.append((A_Tl[i]-fit_Tl.best_fit[i]))
    
plt.plot(mean_times, diff_Bi, 'rv', markersize = 4, label = 'Bi coincidences')
plt.plot(mean_times, diff_Tl, 'bo', markersize = 4, label = 'Tl coincidences')
plt.errorbar(mean_times, diff_Bi, yerr = errorbars_Bi, fmt = 'none', ecolor = 'red')
plt.errorbar(mean_times, diff_Tl, yerr = errorbars_Tl, fmt = 'none', ecolor = 'blue')
plt.xlabel("Time since EOC (days)", fontsize = 16)
plt.ylabel("Residues (kBq)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)

Bi_line = mlines.Line2D([], [], color='red', marker='v', markersize = 4, linestyle = '-', label='Bi coincidence')
Tl_line = mlines.Line2D([], [], color = 'Blue', marker='o', markersize = 4, linestyle = '--', label='Tl coincidences')
plt.legend(handles=[Bi_line, Tl_line])
plt.grid()
plt.show()

"""
# Relative residues
"""
diff_Bi = []
diff_Tl = []
for i in range(len(mean_times)):
    diff_Bi.append(100*(A_Bi[i]-fit_Bi.best_fit[i])/A_Bi[i])
    diff_Tl.append(100*(A_Tl[i]-fit_Tl.best_fit[i])/A_Tl[i])
    
plt.plot(mean_times, diff_Bi, 'rv', markersize = 4, label = 'Bi coincidences')
plt.plot(mean_times, diff_Tl, 'bo', markersize = 4, label = 'Tl coincidences')
plt.errorbar(mean_times, diff_Bi, yerr = 100*errorbars_Bi/A_Bi, fmt = 'none', ecolor = 'red')
plt.errorbar(mean_times, diff_Tl, yerr = 100*errorbars_Tl/A_Tl, fmt = 'none', ecolor = 'blue')
plt.xlabel("Time since EOC (days)", fontsize = 16)
plt.ylabel("Relative residues (%)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)

Bi_line = mlines.Line2D([], [], color='red', marker='v', markersize = 4, linestyle = '-', label='Bi coincidence')
Tl_line = mlines.Line2D([], [], color = 'Blue', marker='o', markersize = 4, linestyle = '--', label='Tl coincidences')
plt.legend(handles=[Bi_line, Tl_line])
plt.grid()
plt.show()
"""
