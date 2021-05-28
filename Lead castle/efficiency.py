import matplotlib.pyplot as plt
from lmfit.models import ExpressionModel
import numpy as np
import copy

# This program fits the absolute efficiency response of the lead castle setup

# energy ordered 245 -> before 276 and 344 -> before 356
# order changes the order of list1 and list2 such that list1 is increasing with index while the indices of list2 change similarly
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


# fitting model
def fit(x, result):
    a = result.params['a'].value
    b = result.params['b'].value
    c = result.params['c'].value
    d = result.params['d'].value
    fit = (1/x)*(a + b*np.log(x) + c*np.log(x)**2 + d*np.log(x)**3)
    return fit

# lists with efficiency in %, energy in kev and their errors
ls_eff_uo = 100 * np.array([0.0006464394302000162, 0.0011053805732230425, 0.000824832, 0.000760593, 0.000649313, 0.00061197, 0.000882007, 0.000652989, 0.000570151, 0.000575505, 0.000298475, 0.000271024, 0.000247721, 0.000228289, 0.00021589, 0.000178684, 0.000191456, 0.00017163])
ls_E_uo= np.array([80.9979, 121.7817, 276.3989, 302.8508, 356.0129, 383.8485, 244.6974, 344.2785, 411.1165, 443.9606, 778.9045, 867.38, 964.057, 1085.837, 1112.076, 1408.013, 1173.228, 1332.492])
#Ba, Eu, 4xBa, 10xEu, 2x cobalt in ordered form
xerr_uo = np.array([0.0011, 0.0003, 0.0012, 0.0005, 0.0007, 0.0012, 0.0008, 0.0012, 0.0012, 0.0016, 0.0024, 0.003, 0.005, 0.01, 0.003, 0.003, 0.0015, 0.002])
yerr_uo = 100 * np.array([0.0001775, 0.0000529, 9.83638E-05, 8.73773E-05, 7.0423E-05, 7.34098E-05, 0.000102896, 7.06373E-05, 9.46763E-05, 7.37844E-05, 3.75467E-05, 3.70748E-05, 3.11823E-05, 3.89277E-05, 2.56202E-05, 1.87296E-05, 3.6E-05, 3.4E-05])

ordered_data = order(ls_E_uo, ls_eff_uo)
ls_E = ordered_data[0]
ls_eff = ordered_data[1]
xerr = order(ls_E, xerr_uo)[1]
yerr = order(ls_E, yerr_uo)[1]


gmod = ExpressionModel("(1/x)*(a + b*ln(x)**1 + c*ln(x)**2 + d*ln(x)**3)")
result = gmod.fit(ls_eff, x = ls_E, a = 1, b = 0, c = 0, d=0, weights = 1/yerr)

plt.plot(ls_E, ls_eff,'o', label = "Data", color = "Black")
plt.errorbar(ls_E, ls_eff, xerr = xerr, yerr = yerr, fmt='k.')
print(result.fit_report())


x = np.linspace(min(ls_E), max(ls_E), 100)
plt.plot(x, fit(x, result), color = 'Blue', label = 'Fit')
delmodel = result.eval_uncertainty(x=x)


# Part to get systematic uncertainty
N = 10000
eps1 = 3/100            # Ba source
eps2 = 4.8/100          # Eu source
eps3 = 3.4/100            # Co source
eff_E = np.zeros((N, 100))
r1 = 1 + np.random.randn(N)*eps1
r2 = 1 + np.random.randn(N)*eps2
r3 = 1 + np.random.randn(N)*eps3



for i in range(len(r1)):
    sources = np.array([r1[i], r2[i], r2[i], r1[i], r1[i], r2[i], r1[i], r1[i], r2[i], r2[i], r2[i], r2[i], r2[i], r2[i], r2[i], r3[i], r3[i], r2[i]])
    ls_temp_eff = sources*ls_eff
    temp_fit = gmod.fit(ls_temp_eff, x = ls_E, a = 1, b = 0, c = 0, d=0, weights = 1/yerr)
    eff_E[i] = fit(x, temp_fit)
    
systematic = np.transpose(eff_E)
ls_lower = np.array([])
ls_upper = np.array([])


for i in range(100):
    errors = np.sort(systematic[i])
    ls_lower = np.append(ls_lower, errors[round(N*0.159)])
    ls_upper = np.append(ls_upper, errors[round(N*(1-0.159))])


#plt.plot(x, ls_lower, color = 'red')
#plt.plot(x, ls_upper, color = 'red')

upper = np.sqrt(ls_upper**2 + delmodel**2)
lower = np.sqrt(ls_lower**2 - delmodel**2)
plt.plot(x, lower, color = 'Red', linewidth = 0.8)
plt.plot(x, upper, color = 'Red', linewidth = 0.8)
plt.fill_between(x, lower, upper, color = 'grey')

#plt.plot(x, (upper - fit(x, result))/fit(x, result))


value = np.array([440.45, 218.12])
bin_value_1 = round((100/(max(ls_E)-min(ls_E))) * (value[0] - 80))
bin_value_2 = round((100/(max(ls_E)-min(ls_E))) * (value[1] - 80))


rel_up_err_1 = (ls_upper[bin_value_1]/fit(x, result)[bin_value_1] - 1)
rel_up_err_2 = (ls_upper[bin_value_2]/fit(x, result)[bin_value_2] - 1)
rel_low_err_1 = (ls_lower[bin_value_1]/fit(x, result)[bin_value_1] - 1)
rel_low_err_2 = (ls_lower[bin_value_2]/fit(x, result)[bin_value_2] - 1)

print(fit(value, result))
print(rel_up_err_1)
print(rel_up_err_2)
print(rel_low_err_1)
print(rel_low_err_2)

print(delmodel[bin_value_1]*100)
print(delmodel[bin_value_2]*100)


"""

diff = []
for i in range(len(ls_E)):
    diff.append(ls_eff[i]-result.best_fit[i])

plt.plot(ls_E, diff, 'o')
plt.errorbar(ls_E, diff, xerr = xerr, yerr = yerr, fmt='k.')
"""


plt.legend(loc = 'best')
plt.xlabel("Energy(keV)", fontsize = 16)
plt.ylabel("Efficiency (%)", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.grid()


