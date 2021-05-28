import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import os.path
from lmfit.models import ExpressionModel

# Single peak fitting program

def function(x, a, b, c):
    f = a * (1 - (x)/((x)**2 + b**2)**(1/2))
    return f

#save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Angular_correlation/Data/'
save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_analysis'
name_of_file = '12-11-2020_14u20_Ba133_25cm_5941.79s'
extension = '.csv'
complete_name = os.path.join(save_path, name_of_file + extension)                       # makes complete path to the file

start_chan = 210                                                   # interval of the peak of interest
end_chan = 230

reader = np.array(pd.read_csv(complete_name, header = 1, sep = ";")).T
E = reader[0][start_chan:end_chan]
count = reader[2][start_chan:end_chan]
E_kev = []

for i in E:
    kev = 2.133 + i * 0.31711 - 2.1*10**(-8)*i**2
    E_kev.append(kev)


gmod = ExpressionModel("amp * exp(-((x - mu)/sigma)**2 / 2) + a - b*x")                 # fit expression, linear addition for electronic noice
result = gmod.fit(count, x = E, amp = 1000, mu = 225 , sigma = 3, a =100, b = 0.1)
A_max = result.params['amp'].value
sigma = result.params['sigma'].value
A_exp = math.sqrt(2 * math.pi) * abs(sigma) * A_max
t = 5941.79
countrate = A_exp/t
error = np.sqrt(2 * np.pi) * sigma*A_max*((result.params['sigma'].stderr/sigma) + (result.params['amp'].stderr/A_max))/t
print(countrate)
print(error)


#print(result.fit_report())
#print(countrate)
plt.grid()
plt.plot(E, count, label = 'data', color = 'Black')                                # we are mainly interested in the mean and standard deviation
plt.xlabel("Channel number", fontsize = 16)
plt.ylabel("Counts", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
#plt.plot(E, result.init_fit, 'k--', label = 'initial fit', color = 'Green')
plt.plot(E, result.best_fit, 'r-', label = 'best fit')
#plt.legend(loc = 'best')
plt.show()

# comparing channel number peaks to their actual value provides an energy scale instead of channel number
# largest peak can be used to calculate the resolution which is given by the FWHM of the gaussian
# for a Gaussian we know FWHM = 2.355 sigma