#cimport agent
#import agent
from agent cimport Agent

from cython cimport view

import numpy as np


cdef class Network:
	def __init__(self, list status_vec, double[::1] lambda_plus_vec, double[::1] lambda_minus_vec, double[::1] infection_risk_vec, double[::1] diagnosis_risk_vec, double[::1] recovery_risk_vec, double warm_up):
		self.agents = self.initialize_agents(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec)
		self.dict = {}
		self.warm_up = warm_up

	cdef public:
		# init
		cpdef list initialize_agents(self, list status_vec, double[::1] lambda_plus_vec, double[::1] lambda_minus_vec, double[::1] infection_risk_vec, double[::1] diagnosis_risk_vec, double[::1] recovery_risk_vec):
			cdef int i 
			cdef list res = list()
			for i in range(len(status_vec)):
				res.append(Agent(i, status_vec[i], lambda_plus_vec[i], lambda_minus_vec[i], infection_risk_vec[i], diagnosis_risk_vec[i], recovery_risk_vec[i]))
			return(res)

		# contact updates
		cpdef double check_edge(self, int i, int j):
			cdef str identifier = str(min(i, j)) + "_" + str(max(i, j))
			try:
				return(self.dict[identifier])
			except:
				return(self.warm_up)
		cpdef double update_edge(self, int i, int j, double t):
			cdef str identifier = str(min(i, j)) + "_" + str(max(i, j))
			self.dict[identifier] = t