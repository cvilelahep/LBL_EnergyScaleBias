import numpy as np

def readContourMap(fname) :
    i_var = []
    j_var = []
    i_true = -1
    j_true = -1
    val = []
    with open(fname, "r") as f :
        for line in f :
            split = line.split()
            if split[0] == "TRUEVALUES" :
                i_true = float(split[1])
                j_true = float(split[2])
            elif split[0] == "CONTOURPOINT" :
                i_var.append(float(split[1]))
                j_var.append(float(split[2]))
                val.append(float(split[3]))
    return np.array(i_var), np.array(j_var), np.array(val), i_true, j_true
