import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import os
import os.path
import copy
from lmfit.models import ExpressionModel

# This program determines the dead time using the decaying source method

def mean_time(start_times, len_sec, decay):         # returns mean time in days
    len_days = len_sec/(24*3600)
    mean_times = np.zeros(len(len_days))
    
    for i in range(len(len_days)):
        mean_times[i] = start_times[i] + len_days[i] + (1/decay)*math.log(decay*len_days[i]) - (1/decay)*math.log(np.exp(decay*len_days[i])-1)
        
    return mean_times


def order(list1, list2):
    ordered = 0
    while ordered == 0:
        ordered = 1
        for i in range(len(list1)):
            a = list1[i]
            b = list1[i-1]
            c = list2[i]
            d = list2[i-1]
            
            if i != 0:
                if a<b:
                    list1[i] = b
                    list1[i-1] = a
                    list2[i] = d
                    list2[i-1] = c
                    
                    ordered = 0
                    
    return[list1, list2]


save_path = 'C:/Users/micha/Documents/school/Master 2e jaar/Masterproef/Data_analysis/Lead Castle/'
filename = 'output.txt'
complete_name = os.path.join(save_path, filename)

reader = np.array(pd.read_csv(complete_name, header = 1, sep = "\t")).T             # load in data
foils = reader[0]
dates = reader[1]
len_s = reader[2]
counts1 = reader[4]
error1 = reader[5]
counts2 = reader[6]
error2 = reader[7]

t_2 = 9.9203                            # half life in days
decay = np.log(2)/t_2                   # decay constant in /days


days_init = np.zeros(len(foils))
day_0 = 5                               # time of collection
month_0 = 11
time_0 = 11*60 + 40 #9:51, 8:51

foil1 = 'm108'
foil2 = 'm118'

for i in range(len(foils)):
    day = float(dates[i].split('/')[0])
    month = float(dates[i].split('/')[1])
    if month == 1:                      # fixes the 31'st day of december and makes january the 13th month
        month += 12
        day += 1
        
    days_init[i] = 30*(month - month_0) + (day - day_0)
 
times_init = np.array([497, 530, 914, 544, 569, 911, 533, 833, 888, 903, 760, 550, 840, 883, 842, 883, 1171, 817, 873, 956, 545, 654, 539, 846, 821, 545, 1133, 1217, 547, 554, 882, 725, 892, 770, 900, 659, 548, 795, 553, 743, 772, 863, 805, 902, 785, 759, 844, 857, 1211, 958, 829, 860])
#times_init = np.zeros(len(foils))       # starting time of measurement
start_times = days_init + (times_init - time_0)/(24*60)       # starting time in days
mean_times = mean_time(start_times, len_s, decay)


t = []
c1 = []
e1 = []
e2 = []
c2 = []
exp_c1 = []
exp_c2 = []

for i in range(0, len(foils)):
    if foils[i] == foil1 and mean_times[i]<45:
        t.append(mean_times[i])
        
        c1.append(counts1[i])#/(0.114))
        c2.append(counts2[i])#/(0.2546))
        e1.append(error1[i])
        e2.append(error2[i])

time1 = copy.deepcopy(t)
time2 = copy.deepcopy(t)
ordered1 = order(time1, c1)
ordered2 = order(time2, c2)

for i in range(len(c1)):
    exp_c1.append(c1[i]*np.exp(decay*(order(time1, time1)[0][i])))
    exp_c2.append(c2[i]*np.exp(decay*(order(time2, time2)[0][i])))
    
t_err = np.exp(decay*(order(time1, time1)[0][i]+(1/(60*24)))) - np.exp(decay*(order(time1, time1)[0][i]))
t_cont = np.linspace(0, max(t), 100)

plt.plot(c2, exp_c2, '.', color = 'blue', label = 'Data')
plt.errorbar(c2, exp_c2, yerr = e2, fmt='none', ecolor = 'blue')
plt.xlabel("Countrate (Hz)", fontsize = 16)
plt.ylabel("Countrate $e^{\lambda t}$ (Hz)", fontsize = 16)
plt.grid()
gmod = ExpressionModel("a -b*x")

fit = gmod.fit(exp_c2, x = c2, a = 100000, b = 0)
a = fit.params['a'].value
b = fit.params['b'].value
a_err = fit.params['a'].stderr
b_err = fit.params['b'].stderr

plt.xticks(size = 12)
plt.yticks(size = 12)



print(fit.fit_report())
print(a)
print(b)
print(10**6*b/a)
print(10**6*(b/a)*np.sqrt(((b_err/b)**2 + (a_err/a)**2)))

#25.66 ns dead time

plt.plot(c2, fit.best_fit, label = 'Fit')
plt.legend(loc = 'best')

#total_counts = np.array([4535700.0, 343811.0, 189581.0, 361189.0, 182413.0, 185911.0, 11000134.0, 4183135.0, 214719.0, 196577.0, 230006.0, 1611303.0, 4326364.0, 188141.0, 181669.0, 262229.0, 10372139.0, 866340.0, 265182.0, 234108.0, 2982719.0, 39749.0, 932709.0, 438019.0, 179771.0, 109619.0, 323246.0, 469641.0, 2537813.0, 143999.0, 251846.0, 1678069.0, 177207.0, 1900061.0, 3254200.0, 1309223.0, 2061474.0, 145743.0, 223150.0, 90522.0, 200487.0, 247729.0, 259208.0, 78755.0, 205881.0, 126938.0, 198355.0, 1185703.0, 5015976.0, 210763.0, 209082.0, 198763.0])


