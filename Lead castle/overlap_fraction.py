from statistics import NormalDist
import numpy as np

# This function calculates the overlap of two Gaussians


eff_218 = (3.48+3.57)/200
eff_440 = (2.9+3.0)/200
I_218 = 2.72/100
I_440 = 0.83/100

fitting1_218 = 1.97/100
fitting1_440 = 1.91/100
fitting2_218 = 1.85/100
fitting2_440 = 1.19/100

rel_1_218 = np.sqrt(fitting1_218**2 + I_218**2 + eff_218**2)
rel_1_440 = np.sqrt(fitting1_440**2 + I_440**2 + eff_440**2)
rel_2_218 = np.sqrt(fitting2_218**2 + I_218**2 + eff_218**2)
rel_2_440 = np.sqrt(fitting2_440**2 + I_440**2 + eff_440**2)


mu1 = 925.9
mu2 = 849.7
sigma1 = mu1 * rel_1_218
sigma2 = mu2 * rel_1_440

print(NormalDist(mu=mu1, sigma=sigma1).overlap(NormalDist(mu=mu2, sigma=sigma2)))


mu1 = 68.7
sigma1 = mu1 * rel_1_440
mu2 = 61.2
sigma2 = mu2 * rel_2_440

print(NormalDist(mu=mu1, sigma=sigma1).overlap(NormalDist(mu=mu2, sigma=sigma2)))
