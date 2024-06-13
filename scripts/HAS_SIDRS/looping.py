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
N = 10000
name = "final/adaptive/cm"
t_max = 1000
sims = 1
seed = 11
warm_up = 0 # can be set to negative value in order to "evolve" network before pandemic hits


# load non looping parameters once:
path_to_parameters = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/parameters/"+name+"/base_parameters"
infection_risk_vec = np.load(path_to_parameters+"/r_inf_vector"+str(N)+".npy")
diagnosis_risk_vec = np.load(path_to_parameters+"/r_diag_vector"+str(N)+".npy")
recovery_risk_vec = np.load(path_to_parameters+"/r_rec_vector"+str(N)+".npy")
sus_risk_vec = np.load(path_to_parameters+"/r_sus_vector"+str(N)+".npy")
lambda_minus_vec = np.load(path_to_parameters+"/lambda_minus_vec"+str(N)+".npy")
lambda_plus_vec = np.load(path_to_parameters+"/lambda_plus_vec"+str(N)+".npy")
status_vec = np.load(path_to_parameters+"/status_vec"+str(N)+".npy").tolist()


init_S = []
init_I = []

for i in range(len(status_vec)):
	if status_vec[i] == "S":
		init_S.append(i)
	else:
		init_I.append(i)


# define loops
#loops_cm = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.33, 0.5, 0.75]
#loops_offset = np.linspace(0,49,15)
#loops_cm = [0.002,0.003,0.004]

#loops_cm = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
#loops_cm_off = [0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]

loops_cm = np.linspace(0,250,251).tolist()
loops_cm_off = np.linspace(0,250,251).tolist()

beta = 0.1


for cm in loops_cm:
	print("Simulating for cm: "+str(cm) +"\n")

	# create results folder "cm_0.01"
	path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling//results/"+name
	path = os.path.join(path_to_results, "cm_"+str(cm))
	try:
		os.mkdir(path) 
	except:
		1 + 1 

	for cm_off in loops_cm_off:
		if cm_off >= cm:
			continue
		print("Simulating for cm_off: "+str(cm_off)+"\n")
		# create results folder "offset_0"
		path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/results/"+name+"/cm_"+str(cm)
		path = os.path.join(path_to_results, "cm_off_"+str(cm_off))
		try:
			os.mkdir(path) 
		except:
			1 + 1 
		path_to_results = "/Users/nilsgubela/Desktop/Projects/Ideas/Simulation speed up/FastStochasticSampling/results/"+name+"/cm_"+str(cm) + "/cm_off_"+str(cm_off)

		# run the simulation
		res_S, res_I, res_D, res_R, res_cum, res_lambda_plus, res_inf_prob = main(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, sus_risk_vec, cm, beta, cm_off, init_S, init_I, warm_up, t_max, sims)

		# save the run
		Z = {}
		for i in range(t_max + 1):
			Z["S"+str(i)] = np.asarray(res_S)[:,i]
			Z["I"+str(i)] = np.asarray(res_I)[:,i]
			Z["D"+str(i)] = np.asarray(res_D)[:,i]
			Z["R"+str(i)] = np.asarray(res_R)[:,i]
			Z["cum"+str(i)] = np.asarray(res_cum)[:,i]
		df = pd.DataFrame(Z)
		df.to_csv(path_to_results+"/has_feat_result_extended_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)

		df_network = pd.DataFrame(np.asarray(res_lambda_plus))
		df_network.to_csv(path_to_results+"/has_feat_network_result_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)
			
		df_inf = pd.DataFrame(np.asarray(res_inf_prob))
		df_inf.to_csv(path_to_results+"/has_feat_inf_result_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)



