import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def time_series(file, counter, cols):
    var_vec = np.zeros((counter, len(cols)))
    min_vec = np.zeros((counter, len(cols)))
    max_vec = np.zeros((counter, len(cols)))
    mean_vec = np.zeros((counter, len(cols)))
    
    file = pd.read_csv(file)
    
    for i in range(counter):
        k = 0
        for col in cols:
            mean_vec[i, k] = np.mean(file[col+str(i)])
            var_vec[i, k] = np.var(file[col+str(i)])
            min_vec[i, k] = np.min(file[col+str(i)])
            max_vec[i, k] = np.max(file[col+str(i)])
            k += 1
    
    return(mean_vec, var_vec, min_vec, max_vec)


cols = ["I", "D", "R"]
counter = 100
N = 100
sims = 1

file = "results/has_feat_result_extended_10000_10_100.csv"
mean_vec1, var_vec1, min_vec1, max_vec1 = time_series(file, counter, cols)

fig, ax = plt.subplots(1,1, figsize = [10, 5])
t = np.linspace(1,counter,  counter)
ax.plot(t,mean_vec1[:,0]+mean_vec1[:,1], color = "red", label = "I+D")
ax.plot(t,mean_vec1[:,1], color = "blue",label = "D")
ax.plot(t,mean_vec1[:,2], color = "forestgreen",label = "R" )

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, ncol = 1,frameon=False)
ax.set_xlim(0,100)
ax.set_xlabel("Time")
ax.set_ylabel("Number of agents")

fig.savefig("results/plot.svg")

