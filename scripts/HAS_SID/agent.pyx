cdef class Agent:
	def __init__(self, int id, str status, double lambda_plus, double lambda_minus, double inf_i, double diag_i, double rec_i): 	#, double sus_i):
		self.id = id
		self.status
		self.parameters = {'lambda_plus': lambda_plus, 'lambda_minus': lambda_minus,
						 'inf_i': inf_i,'diag_i': diag_i, 'rec_i':rec_i} # 	, 'sus_i': sus_i}
		self.lambda_plus = lambda_plus
		self.lambda_minus = lambda_minus
		self.inf_rate = inf_i
		self.infection_risk = 0
		self.diagnosis_risk = 0
		self.recover_risk = 0
		self.infection_time = 0
		#self.sus_risk = 0

	cdef public:
		cpdef void get_infection_risk(self, I_list):
			cdef Agent agent
			cdef double res

			res = 0

			for agent in I_list:
				res += self.lambda_plus*agent.lambda_plus/(self.lambda_plus*agent.lambda_plus + self.lambda_minus*agent.lambda_minus)

			self.infection_risk = self.inf_rate * res

		cpdef Agent select_infected_partner(self, I_list, u):
			cdef Agent agent
			cdef double res

			res = 0
			u *= 1/self.inf_rate

			for agent in I_list:
				res += self.lambda_plus*agent.lambda_plus/(self.lambda_plus*agent.lambda_plus + self.lambda_minus*agent.lambda_minus)
				if res >= u:
					return(agent)

		cpdef void update_risk_added_I(self, Agent agent):
			self.infection_risk += self.inf_rate * self.lambda_plus*agent.lambda_plus/(self.lambda_plus*agent.lambda_plus + self.lambda_minus*agent.lambda_minus)

		cpdef void update_risk_added_R(self, Agent agent):
			self.infection_risk -= self.inf_rate * self.lambda_plus*agent.lambda_plus/(self.lambda_plus*agent.lambda_plus + self.lambda_minus*agent.lambda_minus)


		cpdef void update_risk_added_D(self, Agent agent, beta):
			self.infection_risk -= self.inf_rate * self.lambda_plus* 1/beta * agent.lambda_plus/(self.lambda_plus* 1/beta * agent.lambda_plus + self.lambda_minus*agent.lambda_minus)
			self.infection_risk += self.inf_rate * self.lambda_plus* agent.lambda_plus/(self.lambda_plus* agent.lambda_plus + self.lambda_minus*agent.lambda_minus)

		cpdef void become_infected(self, t):
			self.status = "I"
			self.inf_rate = 0
			self.infection_risk = 0
			self.diagnosis_risk = self.parameters["diag_i"]
			self.recover_risk = self.parameters["rec_i"]
			self.infection_time = t

		cpdef void become_diagnosed(self, beta):
			self.status = "D"
			self.diagnosis_risk = 0
			self.lambda_plus *= beta

		cpdef void become_recovered(self):
			self.status = "R"
			self.lambda_plus = self.parameters["lambda_plus"]
			self.infection_risk = 0
			self.diagnosis_risk = 0
			self.infection_time = 0
			#self.sus_risk = self.parameters["sus_i"]