import numpy as np
from tools import *
import pandas as pd

# necessary parameters
N = 10000

name = "final/adaptive/strategy/bottom_only"
#infected_0 = 10
#path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/results/scenarios_final/network/"+name
path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/results/"+name
t_max = 80
sims = 10
seed = 11
warm_up = 0 # can be set to negative value in order to "evolve" network before pandemic hits 

# adaptive parameters
beta = 0.01

# load parameters from files
name_param = name
path_to_parameters = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/parameters/"+name_param

# fast simulation or extensive simulation
fast = False

np.random.seed(seed)

infection_risk_vec = np.load(path_to_parameters+"/r_inf_vector.npy")
diagnosis_risk_vec = np.load(path_to_parameters+"/r_diag_vector.npy")
recovery_risk_vec = np.load(path_to_parameters+"/r_rec_vector.npy")
lambda_minus_vec = np.load(path_to_parameters+"/lambda_minus_vec.npy")
lambda_plus_vec = np.load(path_to_parameters+"/lambda_plus_vec.npy")
status_vec = np.load(path_to_parameters+"/status_vec.npy").tolist()


init_S = []
init_I = []

for i in range(len(status_vec)):
	if status_vec[i] == "S":
		init_S.append(i)
	else:
		init_I.append(i)




