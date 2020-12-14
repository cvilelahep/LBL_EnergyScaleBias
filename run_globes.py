import sys

from subprocess import Popen
from multiprocessing import Pool

import numpy as np

N_PROCS = 8

OUT_GLOBES_DIR="globes_out/"
EXE_NAME = "./erec_bias_dune"

def runFit(command) :
    if len(command) == 4 :
        outFname = "{0}contour_{1}_Profile_{2}_bias_{3}.dat".format(OUT_GLOBES_DIR, command[1], command[2], command[3])
    elif len(command) == 5 :
        outFname = "{0}contour_{1}_Profile_{2}_bias_{3}_dcp_{4}.dat".format(OUT_GLOBES_DIR, command[1], command[2], command[3], command[4])
    with open(outFname, "w") as f :
        p = Popen(command, stdout = f)
        p.wait()

        
if __name__ == "__main__" :

    if len(sys.argv) < 2 :
        print("Takes one argument, either \"contours\" or \"dcp_scan\"")
        exit(-1)
    
    if sys.argv[1] == "contours" :
        commands = [[EXE_NAME, "dcp_th13", "1", "0.0"],
                    [EXE_NAME, "dcp_th13", "0", "0.0"],
                    [EXE_NAME, "dcp_th13", "1", "0.1"],
                    [EXE_NAME, "dcp_th13", "0", "0.1"],
                    [EXE_NAME, "sinsqth23_dmsq32", "1", "0.0"],
                    [EXE_NAME, "sinsqth23_dmsq32", "0", "0.0"],
                    [EXE_NAME, "sinsqth23_dmsq32", "1", "0.1"],
                    [EXE_NAME, "sinsqth23_dmsq32", "0", "0.1"]]

    elif sys.argv[1] == "dcp_scan" :
        commands = [ [EXE_NAME, "dcp_th13", "1", "0.1", "{0}".format(dcp)] for dcp in np.linspace(0, 2*np.pi, 20) ] 
        commands = commands + [ [EXE_NAME, "dcp_th13", "0", "0.1", "{0}".format(dcp)] for dcp in np.linspace(0, 2*np.pi, 20) ] 
    else :
        print("Unknown argument, must be either \"contours\" or \"dcp_scan\"")
        exit(-1)

    print(commands)
        
    with Pool(N_PROCS) as p :
        p.map(runFit, commands)

    
#    procs = []
#    for command in commands :
#        procs.append(Process(target = runFit, args = (command,)))
#        procs[-1].start()
#        procs[-1].join()

        



    
