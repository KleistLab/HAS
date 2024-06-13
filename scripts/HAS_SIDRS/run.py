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
print("Mode: Extended sampling with diagnosis strategy")
print("Start HAS algorithm...")

# start simulation
start = time.time()


res_S, res_I, res_D, res_R, res_cum, res_lambda_plus, res_inf_prob = main(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, sus_risk_vec, cm, beta, cm_off, init_S, init_I, warm_up, t_max, sims)

end = time.time()
print("Computing time for HAS:")
print(end - start) 


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