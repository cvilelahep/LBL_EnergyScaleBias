from subprocess import Popen
from multiprocessing import Pool

N_PROCS = 8

OUT_GLOBES_DIR="globes_out/"
EXE_NAME = "./erec_bias_dune"

def runFit(command) :
    outFname = "{0}contour_{1}_Profile_{2}_bias_{3}.dat".format(OUT_GLOBES_DIR, command[1], command[2], command[3]) 
    with open(outFname, "w") as f :
        p = Popen(command, stdout = f)
        p.wait()

        
if __name__ == "__main__" :

    commands = [[EXE_NAME, "dcp_th13", "1", "0.0"],
                [EXE_NAME, "dcp_th13", "0", "0.0"],
                [EXE_NAME, "dcp_th13", "1", "0.1"],
                [EXE_NAME, "dcp_th13", "0", "0.1"],
                [EXE_NAME, "sinsqth23_dmsq32", "1", "0.0"],
                [EXE_NAME, "sinsqth23_dmsq32", "0", "0.0"],
                [EXE_NAME, "sinsqth23_dmsq32", "1", "0.1"],
                [EXE_NAME, "sinsqth23_dmsq32", "0", "0.1"]]

    with Pool(N_PROCS) as p :
        p.map(runFit, commands)

    
#    procs = []
#    for command in commands :
#        procs.append(Process(target = runFit, args = (command,)))
#        procs[-1].start()
#        procs[-1].join()

        



    
