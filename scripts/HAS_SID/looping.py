import numpy as np
#import copy
import time
import pandas as pd
import sys
import pickle 
import os 
from tools import *



from main import *

# main parameters
N = 100
name = "manuscript/speed/lambda_plus"
infection_prop = 0.5
recovery = 0
diagnosis_prop = 0
beta = 0.5
t_max = 100000
sims = 1000
seed = 11
warm_up = 0 # can be set to negative value in order to "evolve" network before pandemic hits 

#loops = [infection_prop/10, infection_prop, infection_prop*10, infection_prop * 100, infection_prop * 1000]

loops = []

for i in range(10):
	for k in [-2]:
		loops.append(infection_prop * i * 10**k)

loops = list(set(loops))
loops.sort()
loops.pop(0)
print(loops)

loops = [infection_prop/100]

# created fixed parameters
lambda_minus = 1
diagnosed_0 = 0
infected_0 = 10



# exp+1 distribution
mu_parameter = 1
mu = np.around(1/(1/mu_parameter) * np.log(1/np.random.rand(N))) + 1 # shifted by 1, s.t. mu_i > 0
#mu = np.round(np.random.exponential(mu_parameter, N), 1)
# ones
#mu_mean = 2
#mu = np.ones(N) * mu_mean
# uniform distribution
#mu_mean = 3/2
#mu = np.zeros(N)
#while abs(np.mean(mu) - mu_mean) > 0.0001:
#	mu = np.round(np.random.rand(N)/0.5 * mu_mean, 1)
#print(np.mean(mu))
# scale free
#mu = np.round(np.random.rand(N)**(-2/5),1)

#r_i_vec = np.round(np.random.rand(N), 5) * infection_prop
infection_risk_vec = np.ones(N) * infection_prop
#r_i_vec = np.round(np.random.rand(N), 5)/(infection_prop - infection_prop_min) + infection_prop_min
diagnosis_risk_vec = np.round(np.random.rand(N), 5) * diagnosis_prop
#diagnosis_risk_vec = np.ones(N) * diagnosis_prop
#diag_vec = np.round(np.random.rand(N), 5)/(diagnosis_prop - diag_min) + diag + diag_min

print("Infection rates initialized.")


# contact rates
lambda_plus_vec = get_rates(mu)
lambda_minus_vec = np.ones(N) * lambda_minus # for now: all relationships hold for one month

print("Network rates initialized.")

# initial status 
status_vec = ["S"] * N
status_vec[:infected_0] = ["I"] * infected_0

#recovery_risk_vec = np.ones(N) * recovery

init_S = []
init_I = []

for i in range(len(status_vec)):
	if status_vec[i] == "S":
		init_S.append(i)
	else:
		init_I.append(i)



print("Looping started...")

for loop in loops:

	recovery = loop
	recovery_risk_vec = np.ones(N) * recovery


	#tmp_name = name + str(loop)
	# create parameter path
	path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/results/"+name
	path = os.path.join(path_to_results, "rec"+str(loop))
	try:
		os.mkdir(path) 
	except:
		1 +1 
	path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/results/"+name+"/rec"+str(loop)

	# create result path
	path_to_parameters = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/parameters/"+name
	path = os.path.join(path_to_parameters, "rec"+str(loop))
	try:
		os.mkdir(path) 
	except:
		1 +1 
	path_to_parameters = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/parameters/"+name+"/rec"+str(loop)


	# save parameters
	#np.save(path_to_parameters+"/mu"+str(N)+".npy", mu)
	np.save(path_to_parameters+"/r_inf_vector"+str(N)+".npy", infection_risk_vec)
	np.save(path_to_parameters+"/r_diag_vector"+str(N)+".npy", diagnosis_risk_vec)
	np.save(path_to_parameters+"/partnerships"+str(N)+".npy", list())
	np.save(path_to_parameters+"/lambda_minus_vec"+str(N)+".npy", lambda_minus_vec)
	np.save(path_to_parameters+"/lambda_plus_vec"+str(N)+".npy", lambda_plus_vec)
	np.save(path_to_parameters+"/status_vec"+str(N)+".npy", status_vec)
	np.save(path_to_parameters+"/r_rec_vector"+str(N)+".npy", recovery_risk_vec)


	# start simulation
	start = time.time()

	res_S, res_I, res_D, res_R, res_steps = main_fast(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, beta, init_S, init_I, warm_up, t_max, sims)
	# save run time
	with open(path_to_results+'/has_run_time_'+str(N)+'.txt', 'w') as f:
		f.write(str(time.time() - start))

	df = pd.DataFrame({"S" : np.asarray(res_S), "I": np.asarray(res_I), "D": np.asarray(res_D), "R": np.asarray(res_R), "steps": np.asarray(res_steps)})
	


	df.to_csv(path_to_results+"/has_result_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)

