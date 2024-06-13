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

# load parameters from files?
load_params = True
name_param = name
path_to_parameters = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/parameters/"+name_param

# fast simulation or extensive simulation
fast = False

np.random.seed(seed)

if load_params:
	#mu = np.load(path_to_parameters+"/mu"+str(N)+".npy")
	infection_risk_vec = np.load(path_to_parameters+"/r_inf_vector"+str(N)+".npy")
	diagnosis_risk_vec = np.load(path_to_parameters+"/r_diag_vector"+str(N)+".npy")
	recovery_risk_vec = np.load(path_to_parameters+"/r_rec_vector"+str(N)+".npy")
	#partnerships = np.load(path_to_parameters+"/partnerships"+str(N)+".npy").tolist()
	lambda_minus_vec = np.load(path_to_parameters+"/lambda_minus_vec"+str(N)+".npy")
	lambda_plus_vec = np.load(path_to_parameters+"/lambda_plus_vec"+str(N)+".npy")
	status_vec = np.load(path_to_parameters+"/status_vec"+str(N)+".npy").tolist()


else:
	
	lambda_minus = 1
	infection_prop = 0.1
	diagnosis_prop = 1/(3.5)
	diagnosed_0 = 0
	infected_0 = 10
	recovery = 1/7

	#infection_prop_min = 0.01
	#diag_min = 0.1

	# exp+1 distribution
	mu_parameter = 20
	mu = np.around(1/(1/mu_parameter) * np.log(1/np.random.rand(N))) + 1 # shifted by 1, s.t. mu_i > 0
	#mu = np.round(np.random.exponential(mu_parameter, N), 1)
	# ones
	#mu_mean = mu_parameter
	#mu = np.ones(N) * mu_mean
	# uniform distribution
	#mu_mean = mu_parameter
	#mu = np.zeros(N)
	#while abs(np.mean(mu) - mu_mean) > 0.0001:
	#	mu = np.round(np.random.rand(N)/0.5 * mu_mean, 1)
	#print(np.mean(mu))
	# scale free
	#mu = np.round(np.random.rand(N)**(-2/5),1)

	#infection_risk_vec = np.round(np.random.rand(N), 5) * infection_prop
	infection_risk_vec = np.ones(N) * infection_prop
	#r_i_vec = np.round(np.random.rand(N), 5)/(infection_prop - infection_prop_min) + infection_prop_min
	#diagnosis_risk_vec = np.round(np.random.rand(N), 5) * diagnosis_prop
	diagnosis_risk_vec = np.ones(N) * diagnosis_prop
	#diag_vec = np.round(np.random.rand(N), 5)/(diagnosis_prop - diag_min) + diag + diag_min

	print("Infection rates initialized.")


	# contact rates
	lambda_plus_vec = get_rates(mu)
	lambda_minus_vec = np.ones(N) * lambda_minus # for now: all relationships hold for one month

	#lambda_plus_vec *= 1/10

	print("Network rates initialized.")

	# initial status 
	status_vec = ["S"] * N
	status_vec[:infected_0] = ["I"] * infected_0



	recovery_risk_vec = np.ones(N) * recovery



	# save parameters
	#np.save(path_to_parameters+"/mu"+str(N)+".npy", mu)
	np.save(path_to_parameters+"/r_inf_vector"+str(N)+".npy", infection_risk_vec)
	np.save(path_to_parameters+"/r_diag_vector"+str(N)+".npy", diagnosis_risk_vec)
	np.save(path_to_parameters+"/partnerships"+str(N)+".npy", list())
	np.save(path_to_parameters+"/lambda_minus_vec"+str(N)+".npy", lambda_minus_vec)
	np.save(path_to_parameters+"/lambda_plus_vec"+str(N)+".npy", lambda_plus_vec)
	np.save(path_to_parameters+"/status_vec"+str(N)+".npy", status_vec)
	np.save(path_to_parameters+"/r_rec_vector"+str(N)+".npy", recovery_risk_vec)



init_S = []
init_I = []

for i in range(len(status_vec)):
	if status_vec[i] == "S":
		init_S.append(i)
	else:
		init_I.append(i)




