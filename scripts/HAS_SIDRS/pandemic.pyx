import numpy as np

from libc.math cimport exp 

from cython cimport view

# random number generator
from libc.stdlib cimport rand
cdef extern from "limits.h":
	int INT_MAX

# logarithm
cdef extern from "math.h":
	double log(double x) nogil

# fast sum
cdef double sum_tmv(double[::1] arr):
	cdef size_t i, I
	cdef double total = 0
	I = arr.shape[0]
	for i in range(I):
		total += arr[i]
	return total

from agent cimport Agent
from network cimport Network


cdef class Pandemic:
	def __init__(self, Network network, int cm, double beta, int cm_off, list init_S, list init_I, double warm_up):
		self.network = network
		self.beta = beta
		self.r_inf = 0
		self.r_diag = 0
		self.r_rec = 0
		self.r_sus = 0
		self.warm_up = warm_up
		#self.r_sus = 0
		self.I_list = self.initialize_inf(init_I)
		self.S_list = self.initialize_sus(init_S)
		self.D_list = list()
		self.R_list = list()
		self.cm = cm
		#self.t_offset = t_offset
		self.cm_off = cm_off
		self.measure_active = False
		self.cumm_cases = len(self.I_list)


	cdef public:
		# init 
		cpdef list initialize_sus(self, init_S):
			cdef list res = list()
			cdef Agent agent
			cdef int i = 0
			for i in init_S:
				agent = self.network.agents[i]
				agent.get_infection_risk(self.I_list)
				self.r_inf += agent.infection_risk
				res.append(agent)
			return(res)

		cpdef list initialize_inf(self, init_I):
			cdef list res = list()
			cdef Agent agent
			cdef int i = 0
			for i in init_I:
				agent = self.network.agents[i]
				agent.become_infected(self.warm_up)
				self.r_diag += agent.diagnosis_risk
				self.r_rec += agent.recover_risk
				res.append(agent)
			return(res)

		# pandemic actions
		cpdef void infection(self, double u, double t):
			cdef double tmp_sum 
			cdef int id_S
			cdef Agent agent_I, agent_S
			cdef double delta_t, lambda_exp, c1, edge_prob_t

			# select susceptible agent
			tmp_sum = 0
			id_S = 0
			while tmp_sum < u:
				tmp_sum += self.S_list[id_S].infection_risk
				id_S += 1

			tmp_sum -= self.S_list[id_S-1].infection_risk
			agent_S = self.S_list[id_S - 1]

			# select infected agent
			u -= tmp_sum
			agent_I = agent_S.select_infected_partner(self.I_list + self.D_list, u)


			# check if edge between both agents still exists:
			lambda_exp = agent_I.lambda_plus*agent_S.lambda_plus + agent_I.lambda_minus*agent_S.lambda_minus
			c1 = agent_I.lambda_plus*agent_S.lambda_plus/(lambda_exp)

			# get time between last observation
			delta_t = max(t - self.network.check_edge(agent_I.id, agent_S.id), 0)

			# sample leaped rejection event 
			e_x = agent_S.parameters["inf_i"]*(1 - c1)
			#delta_tx = np.random.exponential(1/e_x)
			delta_tx = 1/e_x * log(float(INT_MAX) / rand())
			# there was no leaped rejection step if the infection just happend 
			if t - agent_I.infection_time < delta_tx:
				delta_tx = delta_t

			edge_prob_t = 1 - exp(-lambda_exp * min(delta_t, delta_tx) )

			#if edge_prob_t >= np.random.rand(): 
			if edge_prob_t >= rand() / float(INT_MAX):
				# infect agent_S
				agent_S.become_infected(t)

				# change lists
				self.I_list.append(agent_S)
				self.S_list.pop(id_S - 1)
				self.cumm_cases += 1

				# increase infection risk for all S
				self.r_inf = 0
				for agent in self.S_list:
					agent.update_risk_added_I(agent_S)
					self.r_inf += agent.infection_risk

				# update diag and rec propensities
				self.r_diag += agent_S.parameters["diag_i"]
				self.r_rec += agent_S.parameters["rec_i"]

				# update edge dict
				# sample the time for which the edge is in place
				self.network.update_edge(agent_I.id, agent_S.id, t + 1/agent_I.lambda_minus*agent_S.lambda_minus * log(float(INT_MAX) / rand()))

			else:
				# update edge dict
				self.network.update_edge(agent_I.id, agent_S.id, t)



		cpdef void diagnosis(self, double u, double t):
			cdef double tmp
			cdef int id_I 
			cdef Agent agent_I, agent

			# select infected agent to receive the diagnosis
			tmp_sum = 0
			id_I = 0
			while tmp_sum < u:
				tmp_sum += self.I_list[id_I].diagnosis_risk
				id_I += 1

			agent_I = self.I_list[id_I - 1]

			# receive diagnosis
			agent_I.become_diagnosed(self.beta)

			# remove all contacts/reset all timers (to S) and decrease infection risk for all S
			self.r_inf = 0
			for agent in self.S_list:
				agent.update_risk_added_D(agent_I, self.beta)
				self.r_inf += agent.infection_risk
				self.network.update_edge(agent_I.id, agent.id, t)

			# change lists
			self.D_list.append(agent_I)
			self.I_list.pop(id_I-1)

			# update diagnosis rate
			self.r_diag -= agent_I.parameters["diag_i"]

			# check if measure kicks in
			if len(self.D_list) >= self.cm and self.measure_active == False:
				# activate measure
				self.measure_active = True
				# All people in I and S need to cut their contacts
				for agent in self.S_list + self.I_list:
					agent.lambda_plus *= self.beta

				# Update all infection risk from I/D to S
				self.r_inf = 0
				for agent in self.S_list:
					agent.get_infection_risk(self.I_list + self.D_list)
					self.r_inf += agent.infection_risk


		cpdef void recovery(self, double u, double t):
			cdef double tmp
			cdef int id_I 
			cdef Agent agent_I, agent
			cdef list tmp_list

			# select I or D to recover
			tmp_list = self.I_list + self.D_list
			tmp_sum = 0
			id_I = 0

			while tmp_sum < u:
				tmp_sum += tmp_list[id_I].recover_risk
				id_I += 1

			agent_I = tmp_list[id_I - 1]

			# remove risk of infection from agent_I
			self.r_inf = 0
			for agent in self.S_list:
				agent.update_risk_added_R(agent_I)
				self.r_inf += agent.infection_risk

			# change lists
			self.R_list.append(agent_I)
			if agent_I.status == "I":
				self.I_list.pop(self.I_list.index(agent_I))
			else:
				self.D_list.pop(self.D_list.index(agent_I))

			# update diagnosis, recovery risk and susceptible risk
			self.r_diag -= agent_I.diagnosis_risk
			self.r_rec -= agent_I.recover_risk
			self.r_sus += agent_I.parameters["sus_i"]

			# recover
			agent_I.become_recovered()

			# check if measure can be lifted
			if len(self.D_list)<=self.cm_off and self.measure_active == True:
				# lift measure
				self.measure_active = False
				# Give people in I and S the contacts back
				for agent in self.S_list + self.I_list:
					agent.lambda_plus = agent.parameters["lambda_plus"]

				# Update all infection risk from I/D to S
				self.r_inf = 0
				for agent in self.S_list:
					agent.get_infection_risk(self.I_list + self.D_list)
					self.r_inf += agent.infection_risk

		cpdef void susceptible(self, double u):
			cdef double tmp
			cdef int id_R 
			cdef Agent agent_R, agent

			# select R to become susceptible
			tmp_sum = 0
			id_R = 0

			while tmp_sum < u:
				tmp_sum += self.R_list[id_R].parameters["sus_i"]
				id_R += 1

			agent_R = self.R_list[id_R - 1]

			# change state and update lists
			self.S_list.append(agent_R)
			self.R_list.pop(id_R-1)
			
			# make sus
			agent_R.become_susceptible()
			# change behaviour if measure is active
			if self.measure_active:
				agent_R.lambda_plus *= self.beta

			# change infection rates
			agent_R.get_infection_risk(self.I_list + self.D_list)
			self.r_inf += agent_R.infection_risk
			self.r_sus -= agent_R.parameters["sus_i"]




