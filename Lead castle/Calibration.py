import matplotlib.pyplot as plt
from lmfit.models import ExpressionModel
from lmfit.models import Model
import numpy as np

# This program performs the energy calibration for the lead castle

ls_chan = [223.476, 266.777, 353.768, 399.325, 1692.073, 1953.032, 171.599, 334.581, 444.01, 497.83, 1046.25, 1191.05, 1349.589, 1549.13, 1591.98, 2076.771]
ls_E = [276.3989, 302.8508, 356.0129, 383.8485, 1173.228, 1332.492, 244.6974, 344.2785, 411.1165, 443.9606, 778.9045, 867.38, 964.057, 1085.837, 1112.076, 1408.013]

xerr = [0.005, 0.004, 0.003, 0.007, 0.004, 0.004, 0.007, 0.005, 0.03, 0.02, 0.01, 0.03, 0.009, 0.04, 0.02, 0.005]
yerr = [0.0012, 0.0005, 0.0007, 0.0012, 0.003, 0.004, 0.0008, 0.0012, 0.0012, 0.0016, 0.0024, 0.003, 0.005, 0.01, 0.003, 0.003]


gmod1 = ExpressionModel("a + b*x") 
gmod2 = ExpressionModel("a + b*x + c*x**2") 

result1 = gmod1.fit(ls_E, x = ls_chan, a = 1, b = 1/3)
result2 = gmod2.fit(ls_E, x = ls_chan, a = 1, b = 1/3, c = 0)

print(result1.fit_report())
print(result2.fit_report())
plt.xticks(size = 12)
plt.yticks(size = 12)


# Plot the residues
"""
diff1 = []
diff2 = []
for i in range(len(ls_E)):
    diff1.append(ls_E[i]-result1.best_fit[i])
    diff2.append(ls_E[i]-result2.best_fit[i])
    
plt.xlabel("Channel number", fontsize = 16)
plt.ylabel("Residual energy (keV)", fontsize = 16)
plt.plot(ls_chan, diff1, 'o', label = "Linear fit", color = "Blue")
plt.errorbar(ls_chan, diff1, xerr = xerr, yerr = yerr, fmt='k.')
plt.plot(ls_chan, diff2, 's', label = "Quadratic fit", color = 'Red')
plt.errorbar(ls_chan, diff2, xerr = xerr, yerr = yerr, fmt='k.')
"""


# Plot the total values
"""
plt.xlabel("Channel number", fontsize = 16)
plt.ylabel("Energy (keV)", fontsize = 16)

plt.plot(ls_chan, ls_E, 'o', label = "Data", color = "Black")
#plt.plot(ls_chan, result1.best_fit, label = "Linear fit", color = "Blue")
plt.plot(ls_chan, result2.best_fit, label = "Quadratic fit", color = "Red")
plt.errorbar(ls_chan, ls_E, xerr = xerr,yerr = yerr, fmt='k.', color = 'Blue')
#plt.plot(ls_chan, result1.init_fit, 'k--', label = 'initial fit', color = 'Green')
#plt.plot(ls_chan, result1.best_fit, 'r-', label = 'best fit')
"""


plt.legend(loc = 'best')
plt.grid()