import numpy as np
from tools import *
import pandas as pd

# necessary parameters
N = 10000

name = "demo"
path_to_results = "demo/results"
t_max = 100
sims = 10
seed = 11
warm_up = 0 # can be set to negative value in order to "evolve" network before pandemic hits 

beta = 0.01

# load parameters from files
path_to_parameters = "demo/parameters"


np.random.seed(seed)


infection_risk_vec = np.load(path_to_parameters+"/r_inf_vector.npy")
diagnosis_risk_vec = np.load(path_to_parameters+"/r_diag_vector.npy")
recovery_risk_vec = np.load(path_to_parameters+"/r_rec_vector.npy")
sus_risk_vec = np.load(path_to_parameters+"/r_sus_vector.npy")
lambda_minus_vec = np.load(path_to_parameters+"/lambda_minus_vec.npy")
lambda_plus_vec = np.load(path_to_parameters+"/lambda_plus_vec.npy")
status_vec = np.load(path_to_parameters+"/status_vec.npy").tolist()

cm = N
cm_off = N


init_S = []
init_I = []

for i in range(len(status_vec)):
	if status_vec[i] == "S":
		init_S.append(i)
	else:
		init_I.append(i)