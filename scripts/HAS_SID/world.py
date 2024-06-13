
import numpy as np

from agent import Agent
from pandemic import Pandemic
from network import Network

class World:
    def __init__(self, lambda_plus_vec, lambda_minus_vec, r_i_vec, partnerships, init_status, diag_vec, beta, t_max):
        self.network = Network(lambda_plus_vec, lambda_minus_vec, r_i_vec, diag_vec, partnerships, init_status)
        self.pandemic = Pandemic(self.network, beta)
        self.t = 0
        self.t_max = t_max
        self.steps = 0
    
    # simulation
    def run_world(self):
        t = 0
        while self.t < self.t_max:
            # sum of propensities
            r_0 = self.pandemic.r_inf + self.pandemic.r_inf_unconnected + self.pandemic.r_diag
            # sample next time 
            delta_t = np.random.exponential(1/r_0)
            if self.t + delta_t >= self.t_max:
                break
            self.t += delta_t
            self.step(r_0)

    def step(self, r_0):
        self.steps += 1
        # select next event 
        u = r_0 * np.random.rand()
        
        if u < self.pandemic.r_inf:
            # infection of connected nodes 
            self.pandemic.infection(u, self.t)
        elif u <  self.pandemic.r_inf + self.pandemic.r_inf_unconnected:
            # infection of unconnected nodes 
            self.pandemic.infection_unconnected(u - self.pandemic.r_inf, self.t)
        else:
            # diagnosis
            self.pandemic.diagnosis(u -  self.pandemic.r_inf - self.pandemic.r_inf_unconnected, self.t)







    	

