from agent cimport Agent

cdef class Network:
	cdef public dict dict
	cdef public list agents
	cdef public double warm_up
	# functions
	cpdef list initialize_agents(self, list status_vec, double[::1] lambda_plus_vec, double[::1] lambda_minus_vec, double[::1] infection_risk_vec, double[::1] diagnosis_risk_vec, double[::1] recovery_risk_vec)
	cpdef double check_edge(self, int i, int j)
	cpdef double update_edge(self, int i, int j, double t)