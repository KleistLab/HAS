import numpy as np

from agent cimport Agent
from network cimport Network

cdef class Pandemic:
	cdef public Network network
	cdef public double beta, r_inf, r_diag, r_rec, r_sus, warm_up
	cdef public list I_list, S_list, D_list, R_list
	cdef public int cm, cumm_cases, cm_off
	cdef public bint measure_active
	# functions
	cpdef list initialize_sus(self, init_S)
	cpdef list initialize_inf(self, init_I)
	cpdef void infection(self, double u, double t)
	cpdef void diagnosis(self, double u, double t)
	cpdef void recovery(self, double u, double t)
	cpdef void susceptible(self, double t)