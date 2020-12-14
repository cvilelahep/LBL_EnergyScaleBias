from glob import glob

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from common_tools import *

if __name__ == "__main__" :

    dcp_scan_files_fixed = glob("globes_out/contour_dcp_th13_Profile_0_bias_0.1_dcp_*.dat")
    dcp_scan_files_profiled = glob("globes_out/contour_dcp_th13_Profile_1_bias_0.1_dcp_*.dat")

    true_delta_fixed = []
    true_delta_profiled = []
    
    delta_chi2_fixed = []
    delta_chi2_profiled = []

    bf_bias_fixed = []
    bf_bias_profiled = []

    for f in dcp_scan_files_profiled :
        x, y, chi2, x_true, y_true = readContourMap(f)
        true_delta_profiled.append(y_true)

        true_i = (np.square(y - y_true) + np.square(x - x_true)).argmin()

        delta_chi2_profiled.append(chi2[true_i] - min(chi2))

        bf_i = chi2.argmin()

        bf_bias_profiled.append(y[bf_i] - y_true)

    for f in dcp_scan_files_fixed :
        x, y, chi2, x_true, y_true = readContourMap(f)
        true_delta_fixed.append(y_true)

        true_i = (np.square(y - y_true) + np.square(x - x_true)).argmin()

        delta_chi2_fixed.append(chi2[true_i] - min(chi2))

        bf_i = chi2.argmin()

        bf_bias_fixed.append(y[bf_i]- y_true)


    true_delta_profiled = np.array(true_delta_profiled)
    delta_chi2_profiled = np.array(delta_chi2_profiled)
    bf_bias_profiled = np.array(bf_bias_profiled)
        
    sorted_is_profiled = np.argsort(true_delta_profiled)

    true_delta_fixed = np.array(true_delta_fixed)
    delta_chi2_fixed = np.array(delta_chi2_fixed)
    bf_bias_fixed = np.array(bf_bias_fixed)
        
    sorted_is_fixed = np.argsort(true_delta_fixed)
    
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(true_delta_profiled[sorted_is_profiled] , np.sqrt(delta_chi2_profiled[sorted_is_profiled]), label = "Disapp. params. profiled")
    plt.plot(true_delta_fixed[sorted_is_fixed] ,np.sqrt(delta_chi2_fixed[sorted_is_fixed]), label = "Disapp. params. fixed")
    plt.ylabel(r"$\sqrt{ \chi^2_{true} - \chi^2_{bf} }$")

    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(true_delta_profiled[sorted_is_profiled], bf_bias_profiled[sorted_is_profiled])
    plt.plot(true_delta_fixed[sorted_is_fixed], bf_bias_fixed[sorted_is_fixed])
    plt.ylabel(r"$\delta_{bf} - \delta_{true}$")
    plt.xlabel(r"$\delta_{true}$")
    
    plt.tight_layout()

    plt.savefig("plots_out/delta_bias_summary.png")
    plt.savefig("plots_out/delta_bias_summary.pdf")
    
    plt.show()
        

