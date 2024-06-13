from world cimport World

import numpy as np
import sys


def main(list status_vec, double[::1] lambda_plus_vec, double[::1] lambda_minus_vec, double[::1] infection_risk_vec, double[::1] diagnosis_risk_vec, double[::1] recovery_risk_vec, double[::1] sus_risk_vec, int cm, double beta, int cm_off, list init_S, list init_I, double warm_up, int t_max, int sims):
	cdef double[:,::1] res_I, res_D, res_S, res_lambda_plus
	cdef int i, t, l
	cdef World world

	res_S = np.zeros((sims, t_max + 1))
	res_I = np.zeros((sims, t_max + 1))
	res_D = np.zeros((sims, t_max + 1))
	res_R = np.zeros((sims, t_max + 1))
	res_cum = np.zeros((sims, t_max + 1))
	res_lambda_plus = np.zeros((len(lambda_plus_vec), t_max + 1))
	res_inf_prob = np.zeros((len(lambda_plus_vec), t_max + 1))

	for i in range(sims):
		sys.stdout.write('\r')
		sys.stdout.write("[%-20s] %d%%" % ('='*int((i+1)*20/sims), (i+1)*100/sims))
		#sys.stdout.write(str(i)+"/"+str(sims))
		sys.stdout.flush()
		#world = pickle.load(filehandler)
		world = World(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, sus_risk_vec, cm, beta, cm_off, init_S, init_I, warm_up, 1)
		
		# first step
		res_S[i,0] = len(world.pandemic.S_list)
		res_I[i,0] = len(world.pandemic.I_list)
		res_D[i,0] = len(world.pandemic.D_list)
		res_R[i,0] = len(world.pandemic.R_list)
		res_cum[i,0] = world.pandemic.cumm_cases
		res_lambda_plus[:,0] = lambda_plus_vec

		for l in range(len(lambda_plus_vec)):
			res_inf_prob[l,0] = 0 if status_vec[l] == "S" else 1

		t = 1
		while t <= t_max:
			world.t_max = t
			world.run_world()

			res_S[i,t] = len(world.pandemic.S_list)
			res_I[i,t] = len(world.pandemic.I_list)
			res_D[i,t] = len(world.pandemic.D_list)
			res_R[i,t] = len(world.pandemic.R_list)
			res_cum[i,t] = world.pandemic.cumm_cases

			for agent in world.network.agents:
				res_lambda_plus[agent.id,t] += agent.lambda_plus/sims
				if agent.status == "I" or agent.status == "D":
					res_inf_prob[agent.id,t] += 1/sims

			t += 1
		
	return(res_S, res_I, res_D, res_R, res_cum, res_lambda_plus, res_inf_prob)




