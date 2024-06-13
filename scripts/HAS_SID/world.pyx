from network cimport Network
from pandemic cimport Pandemic

import numpy as np

# random number generator
from libc.stdlib cimport rand
cdef extern from "limits.h":
    int INT_MAX

# logarithm
cdef extern from "math.h":
    double log(double x) nogil


cdef class World:
    def __init__(self, list status_vec, double[::1] lambda_plus_vec, double[::1] lambda_minus_vec, double[::1] infection_risk_vec, double[::1] diagnosis_risk_vec, double[::1] recovery_risk_vec, double beta, list init_S, list init_I, double warm_up, int t_max):
        self.network = Network(status_vec, lambda_plus_vec, lambda_minus_vec, infection_risk_vec, diagnosis_risk_vec, recovery_risk_vec, warm_up)
        self.pandemic = Pandemic(self.network, beta, init_S, init_I, warm_up)
        self.t = 0
        self.t_max = t_max
        self.steps = 0
        self.delta_t_stored = 0
    
    # simulation
    cpdef void run_world(self):
        cdef double r_0, delta_t
        while self.t < self.t_max:
            # sum of propensities
            r_0 = self.pandemic.r_inf + self.pandemic.r_diag + self.pandemic.r_rec
            if abs(r_0) < 10**(-9):
                self.delta_t_stored = delta_t
                break

            # sample next time 
            #delta_t = np.random.exponential(1/r_0)
            if self.delta_t_stored > 0:
                delta_t = self.delta_t_stored
            else:
                delta_t = 1/r_0 * log(float(INT_MAX) / rand())

            if self.t + delta_t >= self.t_max:
                self.delta_t_stored = delta_t
                break

            self.delta_t_stored = 0
            self.t += delta_t
            self.step(r_0)

    cpdef void step(self, double r_0):
        cdef double u
        self.steps += 1
        # select next event 
        #u = r_0 * np.random.rand()
        u = r_0 * rand() / float(INT_MAX)
        
        if u < self.pandemic.r_inf:
            # infection
            self.pandemic.infection(u, self.t)
        elif u <  self.pandemic.r_inf + self.pandemic.r_diag:
            # diagnosis
            self.pandemic.diagnosis(u - self.pandemic.r_inf, self.t)
        else:
            # recovery
            self.pandemic.recovery(u -  self.pandemic.r_inf - self.pandemic.r_diag)