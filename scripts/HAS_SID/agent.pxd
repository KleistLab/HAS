cdef class Agent:
	cdef public int id
	cdef public str status
	cdef public dict parameters 
	cdef public double infection_risk, diagnosis_risk, recover_risk, lambda_plus, lambda_minus, inf_rate, infection_time
	# functions
	cpdef void get_infection_risk(self, I_list)
	cpdef Agent select_infected_partner(self, I_list, u)
	cpdef void update_risk_added_I(self, Agent agent)
	cpdef void update_risk_added_R(self, Agent agent)
	cpdef void update_risk_added_D(self, Agent agent, beta)
	cpdef void become_infected(self, t)
	cpdef void become_diagnosed(self, beta)
	cpdef void become_recovered(self)