'''
This example use standalone mode for the simulation and joblib library to parallel the code.
for the discussios look at [here](https://brian.discourse.group/t/multiprocessing-in-standalone-mode/142/2)

'''
from joblib import Parallel, delayed
from time import time as wall_time
from os import system
from brian2 import *
import os

def clean_directories():
    system("rm -rf standalone*")


def run_sim(tau):
    
    pid = os.getpid()
    directory=f"standalone{pid}"
    set_device('cpp_standalone', directory=directory)
    print(f'RUNNING {pid}')

    G = NeuronGroup(1, 'dv/dt = -v/tau : 1', method='euler')
    G.v = 1

    mon = StateMonitor(G, 'v', record=0)
    net = Network()
    net.add(G, mon)
    net.run(100 * ms)
    res = (mon.t/ms, mon.v[0])

    device.reinit()

    print(f'FINISHED {pid}')
    return res


if __name__ == "__main__":
    
    statr_time = wall_time()
    
    n_jobs = 4
    tau_values = np.arange(10)*ms + 5*ms

    results = Parallel(n_jobs=n_jobs)(map(delayed(run_sim), tau_values))
    print(len(results), len(results[0]), results[0][1].shape)
    

    print("Done in {:10.3f}".format(wall_time() - statr_time))

    for tau_value, (t, v) in zip(tau_values, results):
        plt.plot(t, v, label=str(tau_value))
    plt.legend()
    plt.show()

    clean_directories()