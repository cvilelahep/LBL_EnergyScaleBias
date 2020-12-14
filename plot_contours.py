import matplotlib.pyplot as plt

#                    68.27%    90%    95%
#chi2_critical_2DF = [2.2958, 4.605, 5.991]
chi2_critical_2DF = [2.2958, 5.991]

def readContourMap(fname) :
    i_var = []
    j_var = []
    val = []
    with open(fname, "r") as f :
        for line in f :
            split = line.split()
            if split[0] != "CONTOURPOINT" :
                continue
            i_var.append(float(split[1]))
            j_var.append(float(split[2]))
            val.append(float(split[3]))
    return i_var, j_var, val

def plotContour(fname, **kwargs) :
    x, y, chi2 = readContourMap(fname)
    plt.tricontour(x, y, chi2, levels = [min(chi2)+critical_value for critical_value in chi2_critical_2DF], **kwargs)


if __name__ == "__main__" :

    plt.figure()
    plotContour("globes_out/contour_dcp_th13_Profile_1_bias_0.0.dat", linestyles = 'solid')
    plotContour("globes_out/contour_dcp_th13_Profile_1_bias_0.1.dat", linestyles = 'dashed')
#    plotContour("globes_out/contour_dcp_th13_Profile_0_bias_0.0.dat", linestyles = 'dashdot')
    plotContour("globes_out/contour_dcp_th13_Profile_0_bias_0.1.dat", linestyles = 'dotted')


    plt.figure()
    plotContour("globes_out/contour_sinsqth23_dmsq32_Profile_1_bias_0.0.dat", linestyles = 'solid')
    plotContour("globes_out/contour_sinsqth23_dmsq32_Profile_1_bias_0.1.dat", linestyles = 'dashed')
#    plotContour("globes_out/contour_sinsqth23_dmsq32_Profile_0_bias_0.0.dat", linestyles = 'dashdot')
    plotContour("globes_out/contour_sinsqth23_dmsq32_Profile_0_bias_0.1.dat", linestyles = 'dotted')
    
    plt.show()
