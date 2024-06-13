import numpy as np
#import copy
import time
import pandas as pd
import sys
import pickle 



from inputs import *
#from world import World

from main import *

print("Operation name: "+ name)
print("Number of agents: "+str(len(lambda_plus_vec)))
print("t_max: "+str(t_max))
print("Number of samples: "+str(sims))
if fast:
	print("Mode: Fast sampling till t_max.")
else:
	print("Mode: Extended sampling.")
print("Start HAS algorithm...")

# start simulation
start = time.time()


if fast:
	res_S, res_I, res_D, res_R, res_steps = main_fast(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, beta, init_S, init_I, warm_up, t_max, sims)

	end = time.time()
	print("Computing time for HAS:")
	print(end - start) 

	df = pd.DataFrame({"S" : np.asarray(res_S), "I": np.asarray(res_I), "D": np.asarray(res_D), "R": np.asarray(res_R), "steps": np.asarray(res_steps)})

	# save run time
	with open(path_to_results+'/has_run_time_'+str(N)+'.txt', 'w') as f:
		f.write(str(end - start))

	df.to_csv(path_to_results+"/has_result_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)

else:
	res_S, res_I, res_D, res_R, res_lambda_plus, res_inf_prob = main_extended(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, beta, init_S, init_I, warm_up, t_max, sims)

	end = time.time()
	print("Computing time for HAS:")
	print(end - start) 


	Z = {}
	for i in range(t_max + 1):
		Z["S"+str(i)] = np.asarray(res_S)[:,i]
		Z["I"+str(i)] = np.asarray(res_I)[:,i]
		Z["D"+str(i)] = np.asarray(res_D)[:,i]
		Z["R"+str(i)] = np.asarray(res_R)[:,i]
	df = pd.DataFrame(Z)
	df.to_csv(path_to_results+"/has_result_extended_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)

	df_network = pd.DataFrame(np.asarray(res_lambda_plus))
	df_network.to_csv(path_to_results+"/has_network_result_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)
	
	df_inf = pd.DataFrame(np.asarray(res_inf_prob))
	df_inf.to_csv(path_to_results+"/has_inf_result_"+str(N)+"_"+str(sims)+"_"+str(t_max)+".csv", index=False)