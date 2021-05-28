# This program calculates the gaussian and circular source models using the approximate distribution of particles

import sys
import math
sys.path.append("C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/")
#from reform_srim import reform
from estimate_sd import estimate_sd
from circular_source import circular_source
from gaussian_source import gaussian_source
from total_output import total_output


### User input ###
# note: For small z/rd, the amount of points are made higher for better convergence
rd = math.sqrt(300/math.pi)                         # absolute detector radius in mm
n1 = 10 ** 3                                        # amount of points for the circular integral >10^3 recommended
n_r = 10**2                                         # amount of points for the gaussian integral over r ~10^2 recommended
n_k = 10**2                                         # amount of points for the gaussian integral over k >10^3 recommended
nr_points = 100                                     # distances for which to plot
z_min = 10**-2                                      # minimal z in plotrange in mm, CAN'T BE 0!
z_max = 20                                          # maximal z in plotrange in mm
save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Semi_analytic/'# path to all files (data and python)
name_in = "easyread_60kev"                 # name srim datafile
y_col = 2                                           # index of y column in initial data file
z_col = 3                                           # index of z column in initial data file
name_combined = "output_complete_60realbeam"        # name complete datafile (written in the program)



### buffer locations which are overwritten if the program runs again
name_out = "Semi_analtic/Buffer documents/easyread"              # name easyread srim file (written in the program)
name_circular = "Semi_analtic/Buffer documents/output_circular"  # name datafile circular (written in the program)
name_gaussian = "Semi_analitic/Buffer documents/output_gaussian"  # name datafile gaussian (written in the program)



### Main program ###

if __name__ == "__main__":
    #reform(save_path, name_in, name_out)            # reforms srim data in a more convenient form
    sigma = estimate_sd(save_path, name_out, y_col, z_col)  # calculates standard deviation of the y and z data
    rs = 2 * sigma                                  # estimate for circular approximation
    circular_source(rs, rd, n1, nr_points, z_min, z_max, save_path, name_circular)
    gaussian_source(sigma, rd, n_r, n_k, nr_points, z_min, z_max, save_path, name_gaussian)
    total_output(save_path, name_circular, name_gaussian, name_combined)
    
    