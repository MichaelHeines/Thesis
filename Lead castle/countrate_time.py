import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import os
import os.path
import copy
from lmfit.models import ExpressionModel

# This function uses the obtained count rates and efficiency response to perform an exponential decay fit

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


save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_analysis/Lead Castle/'
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
day_0 = 5 #4 and 5 /11 for 108 and 118                               # time of collection
month_0 = 11
time_0 = 13 + 60*40 #11:00 and 13:40

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
c2 = []


eff = [0.0542593,  0.09480616]
eff1 = eff[1]/100
eff2 = eff[0]/100
ls_used = []

for i in range(0, len(foils)):
    if foils[i] == foil2 and mean_times[i]<40:
        t.append(mean_times[i])
        ls_used.append(i)
        
        c1.append(counts1[i]/(1000*0.114*eff1))
        c2.append(counts2[i]/(1000*0.2546*eff2))
        
e1 = np.array([])
e2 = np.array([])

for i in ls_used:
    e1 = np.append(e1, error1[i])
    e2 = np.append(e2, error2[i])

time1 = copy.deepcopy(t)
time2 = copy.deepcopy(t) 
ordered1 = order(time1, c1)
ordered2 = order(time2, c2)
c1 = ordered1[1]
c2 = ordered2[1]
t_cont = np.linspace(0, max(t), 100)


t_dead = 1.256*10**(-6)
c1_corrected = np.zeros(len(c1))
c2_corrected = np.zeros(len(c2))

for i in range(len(c1)):
    c1_corrected[i] = (c1[i]*1.0565)
    c2_corrected[i] = (c2[i]*1.0565)


errors = np.array([4.5, 3.13])/100
errorbars1 = errors[0]*c1_corrected + e1
errorbars2 = errors[1]*c2_corrected + e2
sys_errors = np.array([-4.43, 4.50, -3.04, 3.13])/100


filename_out = 'activities_pb_M118.csv'
complete_name_out = os.path.join(save_path, filename_out)
fout = open(complete_name_out, "w")
fout.write("t_mean" + ";" + "A 218 " + ";" + "E 218 "  + ";" + "A 440" + ";" + "E 440 "+ "\n")

for i in range(len(time1)):
    fout.write(str(time1[i]) + ";" + str(c1_corrected[i]) + ";" + str(errorbars1[i]) + ";" + str(c2_corrected[i]) + ";" + str(errorbars2[i]) + "\n")

fout.close()


# Fixed half-life

gmod = ExpressionModel("a * exp(-0.0698715946654784*x)")

fit1 = gmod.fit(c1_corrected, x = time1, a = 50000, weights = 1/errorbars1)
a1 = fit1.params['a'].value
resulting_fit1 = a1 * np.exp(- decay * t_cont)
print(a1)

final_error1 = np.sqrt((fit1.params['a'].stderr/a1)**2 + sys_errors[0:2]**2)
print("final " + str(final_error1))
print(fit1.params['a'].stderr/a1)


fit2 = gmod.fit(c2_corrected, x = time2, a = 50000, weights = 1/errorbars2)
a2 = fit2.params['a'].value
resulting_fit2 = a2 * np.exp(- decay * t_cont)
print(a2)

final_error2 = np.sqrt((fit2.params['a'].stderr/a2)**2 + sys_errors[2:4]**2)
print("final " + str(final_error2))
print(fit2.params['a'].stderr/a2)

print(fit1.fit_report())
print(fit2.fit_report())

plt.plot(time1, c1_corrected, '.',color = 'Blue')
plt.plot(time2, c2_corrected, '.',color = 'Red')
plt.errorbar(time1, c1_corrected, yerr = errorbars1, fmt='none', ecolor = 'blue')
plt.errorbar(time1, c2_corrected, yerr = errorbars2, fmt='none', ecolor = 'Red')


plt.plot(t_cont, resulting_fit1, 'b--', label = '218 keV')
plt.plot(t_cont, resulting_fit2, 'r', label = '440 keV')
plt.xlabel("Time since EOC (days)", fontsize = 16)
plt.ylabel("Activity (kBq)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.legend(loc = 'best')
plt.grid()
plt.show()

print(2*(a1-a2)/(a1+a2))

correction = 3.82/(6.32 + 3.82)
A = a1*correction + a2*(1-correction)
print(A)


#variable half-life
"""
gmod = ExpressionModel("a * exp(-b*x)")

fit1 = gmod.fit(c1_corrected, x = time1, a = 50000, b = decay, weights = 1/errorbars1)
a1 = fit1.params['a'].value
b1 = fit1.params['b'].value
resulting_fit1 = a1 * np.exp(- b1 * t_cont)
print(a1)

final_error1 = np.sqrt((fit1.params['a'].stderr/a1)**2 + sys_errors[0:2]**2)
print("final " + str(final_error1))
print(fit1.params['a'].stderr/a1)

print(b1)
print(fit1.params['b'].stderr)

fit2 = gmod.fit(c2_corrected, x = time2, a = 50000, b = decay, weights = 1/errorbars2)
a2 = fit2.params['a'].value
b2 = fit2.params['b'].value 
resulting_fit2 = a2 * np.exp(- b2 * t_cont)
print(a2)

final_error2 = np.sqrt((fit2.params['a'].stderr/a2)**2 + sys_errors[2:4]**2)
print("final " + str(final_error2))
print(fit2.params['a'].stderr/a2)

print(b2)
print(fit2.params['b'].stderr)

print(decay)

plt.plot(time1, c1_corrected, '.',color = 'Blue')
plt.plot(time2, c2_corrected, '.',color = 'Red')
plt.errorbar(time1, c1_corrected, yerr = errorbars1, fmt='none', ecolor = 'blue')
plt.errorbar(time1, c2_corrected, yerr = errorbars2, fmt='none', ecolor = 'Red')


plt.plot(t_cont, resulting_fit1, 'b--', label = '218 keV')
plt.plot(t_cont, resulting_fit2, 'r', label = '440 keV')
plt.xlabel("Time since EOC (days)", fontsize = 16)
plt.ylabel("Activity (kBq)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.legend(loc = 'best')
plt.grid()
plt.show()

print(2*(a1-a2)/(a1+a2))

correction = 3.82/(6.32 + 3.82)
A = a1*correction + a2*(1-correction)
print(A)
"""

# Residues
"""
diff_218 = []
diff_440 = []
for i in range(len(c1_corrected)):
    diff_218.append((c1_corrected[i]-fit1.best_fit[i]))#/c1_corrected[i])
    diff_440.append((c2_corrected[i]-fit2.best_fit[i]))#/c2_corrected[i])

plt.plot(time1, diff_218, 'o', color = 'Blue', label = '218 keV')
plt.errorbar(time1, diff_218, yerr = errorbars1, fmt='k.')
plt.plot(time2, diff_440, 'o', color = 'Red', label = '440 keV')
plt.errorbar(time2, diff_440, yerr = errorbars2, fmt='k.')
plt.xlabel("Time since EOC(days)", fontsize = 16)
plt.ylabel("Residues (kBq)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.legend(loc = 'best')
plt.grid()
plt.show()
"""

# Relative residues
"""
diff_218 = []
diff_440 = []
for i in range(len(c1_corrected)):
    diff_218.append(100*(c1_corrected[i]-fit1.best_fit[i])/c1_corrected[i])
    diff_440.append(100*(c2_corrected[i]-fit2.best_fit[i])/c2_corrected[i])

plt.plot(time1, diff_218, 'o', color = 'Blue', label = '218 keV')
plt.errorbar(time1, diff_218, yerr = 100*errorbars1/c1_corrected, fmt='k.')
plt.plot(time2, diff_440, 'o', color = 'Red', label = '440 keV')
plt.errorbar(time2, diff_440, yerr = 100*errorbars2/c2_corrected, fmt='k.')
plt.xlabel("Time since EOC(days)", fontsize = 16)
plt.ylabel("Relative residues (%)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.legend(loc = 'best')
plt.grid()
plt.show()
"""

