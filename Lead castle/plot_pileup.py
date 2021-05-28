import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import os.path
from lmfit.models import ExpressionModel

# This function plots the pile-up fraction for the lead castle setup

main_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_analysis/Lead Castle/'
filename = 'pileup.txt'

complete_name = os.path.join(main_path, filename)
reader = np.array(pd.read_csv(complete_name, header = 1, sep = "\t")).T

ls_218 = reader[0]
ls_440 = reader[1]
err_218 = reader[2]
err_440 = reader[3]
xvals = np.linspace(0, len(ls_218), len(ls_218))



#plt.plot(ls_218, 'o', color = 'black', label = '218')
#plt.errorbar(xvals, ls_218, yerr = err_218*ls_218, fmt='b.')

plt.plot(ls_440, 'o', color = 'red', label = '440')
plt.errorbar(xvals, ls_440, yerr = err_440*ls_440, fmt='r.')

plt.xlabel('Datapoint', fontsize = 16)
plt.ylabel('Pile-up fraction' , fontsize = 16)

plt.grid()
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.show()




